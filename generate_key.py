from django.core.management.utils import get_random_secret_key

# Generate a new secret key
secret_key = get_random_secret_key()
print('Generated SECRET_KEY:', secret_key)

# Create/update .env file content
env_content = f"""# Django
DJANGO_ENV=development
SECRET_KEY={secret_key}
DEBUG=True

# Database
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=postgres123
DB_NAME=dev
DB_PORT=5432

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Elasticsearch
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_USER=elastic
ELASTICSEARCH_PASSWORD=elastic123
KIBANA_SYSTEM_PASSWORD=elastic123

# RabbitMQ
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
"""

# Write to .env file
with open('.env', 'w') as f:
  f.write(env_content)

print('\nSecret key has been written to .env file')