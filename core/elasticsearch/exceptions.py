"""Elasticsearch-specific exceptions."""

class ESError(Exception):
  """Base exception for Elasticsearch errors."""
  pass

class ESConnectionError(ESError):
  """Raised when Elasticsearch connection fails."""
  pass

class ESOperationError(ESError):
  """Raised when an Elasticsearch operation fails."""
  pass

class ESIndexError(ESError):
  """Raised when index operations fail."""
  pass

class ESBulkOperationError(ESError):
  """Raised when bulk operations fail."""
  pass
