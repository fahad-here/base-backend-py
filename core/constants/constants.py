"""System-wide constants."""
from enum import Enum

class LogEvents(str, Enum):
  LOG_LEVEL_INFO = "LOG_LEVEL_INFO"
  CUSTOMER_REGISTERED = "CUSTOMER_REGISTERED"
  CUSTOMER_LOGIN = "CUSTOMER_LOGIN"
  PASSWORD_CHANGED = "PASSWORD_CHANGED"
  VERIFICATION_CODE_SENT = "VERIFICATION_CODE_SENT"

class BackendResources(str, Enum):
  CUSTOMER = "CUSTOMER"
  ACCOUNT = "ACCOUNT"
  TRANSACTION = "TRANSACTION"
  DOCUMENT = "DOCUMENT"
  IB = "IB"

class ResourceActions(str, Enum):
  CREATE = "CREATE"
  UPDATE = "UPDATE"
  DELETE = "DELETE"
  CHANGE = "CHANGE"

class ResponseMessages:
  RECORD_CREATE_SUCCESS = "Record created successfully"
  RECORD_UPDATE_SUCCESS = "Record updated successfully"
  RECORD_DELETE_SUCCESS = "Record deleted successfully"
  RECORD_FETCH_SUCCESS = "Record fetched successfully"
  INVALID_CREDENTIALS = "Invalid credentials"
  CODE_SENT = "Verification code sent successfully"

# Export constants
LOG_EVENTS = LogEvents
BACKEND_RESOURCES = BackendResources
RESOURCE_ACTIONS = ResourceActions