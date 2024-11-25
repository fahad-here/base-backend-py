from abc import ABC, abstractmethod
from typing import Dict, Any, ClassVar
from django.conf import settings
from core.elasticsearch.constants import DEFAULT_SETTINGS

class BaseIndex:
  INDEX_NAME: ClassVar[str] = None
  SETTINGS: ClassVar[Dict] = DEFAULT_SETTINGS

  @classmethod
  def get_mapping(cls) -> Dict:
    raise NotImplementedError

  @classmethod
  def get_index_name(cls) -> str:
    if cls.INDEX_NAME is None:
        raise NotImplementedError("INDEX_NAME must be set")
    return f"{settings.ELASTICSEARCH_INDEX_PREFIX}_{cls.INDEX_NAME}"

  @classmethod
  def get_settings(cls) -> Dict:
    return cls.SETTINGS

  @classmethod
  @abstractmethod
  def get_document(cls, instance: Any) -> Dict[str, Any]:
    """Convert instance to ES document."""
    pass 