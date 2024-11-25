"""Elasticsearch module initialization."""
from .client import ESClient, es_client

__all__ = ["ESClient", "es_client"]