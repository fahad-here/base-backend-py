"""
Elasticsearch client configuration and management.
"""
from typing import Optional, Dict, Any, List
from elasticsearch import AsyncElasticsearch
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import logging
from shared.utils.logger import logger
from .exceptions import ESConnectionError, ESOperationError, ESBulkOperationError
from .constants import DEFAULT_SETTINGS, MAX_RETRIES, REQUEST_TIMEOUT
from .indices.customer import CustomerIndex
# from .indices.transaction import TransactionIndex

logger = logging.getLogger('elasticsearch')

class ESClient:
    def __init__(self):
        self.connection: Optional[AsyncElasticsearch] = None
        self._initialized = False
        
        # Define indices using the schemas
        self.indices = [
            CustomerIndex,
            # TransactionIndex
        ]

    async def initialize(self) -> None:
        """Initialize Elasticsearch connection if not already initialized."""
        if self._initialized:
            return
            
        if not hasattr(settings, 'ELASTICSEARCH_HOST'):
            raise ImproperlyConfigured("Elasticsearch settings not configured")
            
        await self.connect()
        await self.setup_indices()
        self._initialized = True

    async def ensure_connection(self) -> None:
        """Ensure Elasticsearch connection is established."""
        if not self._initialized:
            await self.initialize()
        elif not self.connection:
            await self.connect()

    async def __aenter__(self):
        await self.ensure_connection()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self) -> None:
        """Establish connection to Elasticsearch."""
        try:
            logger.info(f"Connecting to Elasticsearch at {settings.ELASTICSEARCH_HOST}")
            
            # Base connection config
            connection_config = {
              "hosts": [f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"],
              "verify_certs": False,
              "max_retries": MAX_RETRIES,
              "retry_on_timeout": True,
              "request_timeout": REQUEST_TIMEOUT
            }
            
            # Add authentication if configured
            if hasattr(settings, 'ELASTICSEARCH_USER') and hasattr(settings, 'ELASTICSEARCH_PASSWORD'):
              connection_config["basic_auth"] = (
                settings.ELASTICSEARCH_USER,
                settings.ELASTICSEARCH_PASSWORD
              )
            
            self.connection = AsyncElasticsearch(**connection_config)
            
            # Test connection
            await self.connection.ping()
            logger.info("Elasticsearch connection established successfully")
            
            # Initialize indices
            await self.initialize_indices()
            
        except Exception as e:
            logger.error(f"Failed to connect to Elasticsearch: {str(e)}")
            raise ESConnectionError(f"Elasticsearch connection failed: {str(e)}")

    async def initialize_indices(self) -> None:
        """Initialize all defined indices."""
        for index in self.indices:
            try:
                index_name = index.get_index_name()
                exists = await self.index_exists(index_name)
                
                if not exists:
                    # Only create if index doesn't exist
                    await self.create_index(
                        index_name,
                        index.get_mapping(),
                        index.get_settings()
                    )
                    logger.info(f"Created new index: {index_name}")
                else:
                    # Optionally update mapping for existing index
                    await self.update_index(
                        index_name,
                        index.get_mapping(),
                        index.get_settings()
                    )
                    logger.info(f"Updated existing index: {index_name}")
                    
            except Exception as e:
                logger.error(f"Failed to initialize index {index.get_index_name()}: {str(e)}")
                raise

    async def index_exists(self, index: str) -> bool:
        """Check if an index exists."""
        try:
            return await self.connection.indices.exists(index=index)
        except Exception as e:
            logger.error(f"Failed to check index existence {index}: {str(e)}")
            return False

    async def create_index(self, index: str, mapping: Dict, settings: Dict) -> bool:
        """Create a new index with mapping and settings."""
        try:
            await self.connection.indices.create(
                index=index,
                body={
                  "settings": settings,
                  "mappings": mapping
                }
            )
            logger.info(f"Created index: {index}")
            return True
        except Exception as e:
            logger.error(f"Failed to create index {index}: {str(e)}")
            return False

    async def update_index(self, index: str, mapping: Dict, settings: Dict) -> bool:
        """Update existing index with new mapping and settings."""
        try:
            # Close index
            await self.connection.indices.close(index=index)
            
            # Update settings and mapping
            await self.connection.indices.put_settings(
              index=index,
              body=settings
            )
            await self.connection.indices.put_mapping(
              index=index,
              body=mapping
            )
            
            # Reopen index
            await self.connection.indices.open(index=index)
            
            logger.info(f"Updated index: {index}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update index {index}: {str(e)}")
            await self.connection.indices.open(index=index)
            return False

    async def add_document(self, index: str, id: str, document: Dict[str, Any]) -> bool:
        """Add or update a single document."""
        try:
            await self.ensure_connection()
            await self.connection.index(
                index=index,
                id=id,
                document=document,
                refresh=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to add document to {index}: {str(e)}")
            return False
            
    async def delete_document(self, index: str, id: str) -> bool:
      """Delete a single document by ID."""
      try:
          await self.ensure_connection()
          await self.connection.delete(
              index=index,
              id=id,
              refresh=True
          )
          return True
      except Exception as e:
          logger.error(f"Failed to delete document {id} from {index}: {str(e)}")
          return False

    async def bulk_update(self, index: str, documents: List[Dict[str, Any]]) -> bool:
        """Perform bulk update operation."""
        try:
            operations = []
            for doc in documents:
                operations.extend([
                    {"update": {"_index": index, "_id": doc["id"]}},
                    {"doc": doc, "doc_as_upsert": True}
                ])
            
            response = await self.connection.bulk(
                operations=operations,
                refresh=True
            )
            
            if response.get("errors"):
                self._handle_bulk_errors(response, index, len(documents))
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Bulk update failed for index {index}: {str(e)}")
            return False

    def _handle_bulk_errors(self, response: Dict, index: str, doc_count: int) -> None:
        """Handle bulk operation errors."""
        errored_documents = []
        
        for item in response["items"]:
            if "error" in item.get("update", {}):
                errored_documents.append({
                    "status": item["update"].get("status"),
                    "error": item["update"].get("error"),
                    "id": item["update"].get("_id")
                })
        
        logger.error(
            "Bulk update errors",
            extra={
                "index": index,
                "total_docs": doc_count,
                "failed_docs": len(errored_documents),
                "errors": errored_documents
            }
        )

    async def setup_indices(self) -> None:
      """Setup all indices."""
      try:
        for index in self.indices:
          exists = await self.index_exists(index.get_index_name())
          if not exists:
            await self.create_index(
              index.get_index_name(),
              index.get_mapping(),
              index.get_settings()
            )
      except Exception as e:
        logger.error(f"Failed to setup indices: {str(e)}")
        raise

    async def index(self, index: str, id: str, document: Dict, refresh: bool = False) -> None:
        """Index a document."""
        try:
            await self.ensure_connection()
            await self.connection.index(
                index=index,
                id=id,
                document=document,
                refresh=refresh
            )
        except Exception as e:
            logger.error(f"Failed to add document to {index}: {str(e)}")
            raise ESOperationError(f"Failed to index document: {str(e)}")

    async def get(self, index: str, id: str) -> Dict:
        """Get a document by ID."""
        try:
            await self.ensure_connection()
            return await self.connection.get(
                index=index,
                id=id
            )
        except Exception as e:
            logger.error(f"Failed to get document from {index}: {str(e)}")
            raise ESOperationError(f"Failed to get document: {str(e)}")

    async def search(self, index: str, query: Dict) -> Dict:
        """Search documents."""
        try:
            await self.ensure_connection()
            return await self.connection.search(
                index=index,
                query=query
            )
        except Exception as e:
            logger.error(f"Failed to search in {index}: {str(e)}")
            raise ESOperationError(f"Failed to search documents: {str(e)}")

# Create singleton instance
es_client = ESClient()