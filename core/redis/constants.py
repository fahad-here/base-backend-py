"""Redis-related constants."""

# Key prefixes
USER_PREFIX = "user:"
CUSTOMER_PREFIX = "customer:"
SESSION_PREFIX = "session:"

# Default values
DEFAULT_EXPIRE = 3600  # 1 hour
MAX_CONNECTIONS = 10
SOCKET_TIMEOUT = 5
SCAN_COUNT = 1000

# Login attempt settings
MAX_LOGIN_ATTEMPTS = 5
LOGIN_ATTEMPT_EXPIRE = 3600  # 1 hour