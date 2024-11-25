import pytest
from rest_framework.test import APIClient
from django.conf import settings
from core.elasticsearch.client import es_client
from core.redis import redis_client
from elasticsearch import AsyncElasticsearch
from core.elasticsearch.indices.customer import CustomerIndex

@pytest.fixture
def api_client():
  return APIClient()

@pytest.fixture(scope="function")
async def es_test_client():
    client = AsyncElasticsearch(
        hosts=[f"{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"],
        basic_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD)
    )
    
    # Create test index with mapping
    await client.indices.create(
        index=f"{settings.ELASTICSEARCH_INDEX_PREFIX}_customers",
        mappings=CustomerIndex.get_mapping(),
        settings=settings.ELASTICSEARCH_SETTINGS['default']
    )
    
    yield client
    
    # Cleanup after test
    await client.indices.delete(
        index=f"{settings.ELASTICSEARCH_INDEX_PREFIX}_customers"
    )
    await client.close()

@pytest.fixture
def redis_test_client():
  return redis_client