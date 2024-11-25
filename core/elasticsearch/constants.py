"""Elasticsearch-related constants."""

# Index settings
DEFAULT_SETTINGS = {
  "max_ngram_diff": 19,
  "index": {
    "max_result_window": 10000,
    "queries": {
        "cache": {"enabled": True}
    }
  },
  "analysis": {
    "analyzer": {
      "custom_analyzer": {
        "type": "custom",
        "tokenizer": "standard",
        "filter": ["lowercase", "asciifolding"]
      },
      "autocomplete": {
        "filter": ["lowercase", "autocomplete_filter"],
        "type": "custom",
        "tokenizer": "standard"
      }
    },
    "filter": {
      "autocomplete_filter": {
        "type": "ngram",
        "min_gram": "1",
        "max_gram": "20"
      }
    }
  },
  "number_of_replicas": "1"
}

# Connection settings
MAX_RETRIES = 5
REQUEST_TIMEOUT = 60
BULK_SIZE = 500

# Index prefixes
CUSTOMER_INDEX = "customers"
TRANSACTION_INDEX = "transactions"
