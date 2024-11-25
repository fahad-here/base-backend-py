from typing import Dict, Any
from django.conf import settings
from .base import BaseIndex

class CustomerIndex(BaseIndex):
  INDEX_NAME = 'customers'
  
  @classmethod
  def get_mapping(cls) -> Dict[str, Any]:
    return {
      "properties": {
        "id": {"type": "keyword"},
        "email": {"type": "keyword"},
        "first_name": {
          "type": "text",
          "analyzer": "custom_analyzer",
          "fields": {
            "keyword": {"type": "keyword"}
          }
        },
        "last_name": {
          "type": "text",
          "analyzer": "custom_analyzer",
          "fields": {
            "keyword": {"type": "keyword"}
          }
        },
        "phone": {"type": "keyword"},
        "country": {"type": "keyword"},
        "status": {"type": "keyword"},
        "kyc_status": {"type": "keyword"},
        "agent_id": {"type": "keyword"},
        "profile": {
          "properties": {
            "date_of_birth": {"type": "date"},
            "nationality": {"type": "keyword"},
            "address": {"type": "object"}
          }
        },
        "created_at": {"type": "date"},
        "updated_at": {"type": "date"}
      }
    }
  
  @classmethod
  def get_document(cls, customer) -> Dict[str, Any]:
    return {
      "id": str(customer.id),
      "email": customer.email,
      "first_name": customer.first_name,
      "last_name": customer.last_name,
      "phone": customer.phone,
      "country": customer.country,
      "status": customer.status,
      "kyc_status": getattr(customer, 'kyc_status', None),
      "agent_id": getattr(customer, 'agent_id', None),
      "profile": {
        "date_of_birth": customer.profile.date_of_birth.isoformat() if hasattr(customer, 'profile') and customer.profile.date_of_birth else None,
        "nationality": customer.profile.nationality if hasattr(customer, 'profile') else None,
        "address": customer.profile.address if hasattr(customer, 'profile') else None
      },
      "created_at": customer.created_at.isoformat(),
      "updated_at": customer.updated_at.isoformat()
    } 