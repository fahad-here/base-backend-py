import logging
from datetime import datetime
from typing import Any, Dict

class ESHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            log_entry = self.format_log_entry(record)
            print(f"ES Log: {log_entry}")
        except Exception as e:
            print(f"Failed to log to Elasticsearch: {str(e)}")

    def format_log_entry(self, record: logging.LogRecord) -> Dict[str, Any]:
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'logger': record.name
        }

# Create default logger instance
logger = logging.getLogger('app')
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Elasticsearch handler
es_handler = ESHandler()
logger.addHandler(es_handler) 