# Django Backend Project

A robust Django backend project with Elasticsearch, Redis, and PostgreSQL integration.

## Tech Stack

- Django 5.0.2
- PostgreSQL 15
- Elasticsearch 8.12
- Redis 7
- Python 3.8+

## Project Structure

project/
├── apps/                    # Application modules
│   ├── cp/                 # Customer Portal
│   └── crm/                # CRM Module
├── core/                   # Core configuration
│   ├── settings/           # Environment-specific settings
│   ├── elasticsearch/      # Elasticsearch configuration
│   ├── redis/              # Redis configuration
│   ├── websocket/          # WebSocket configuration
│   └── security/           # Authentication and authorization configuration
├── models/                 # Database models
├── shared/                 # Shared utilities
└── docker/                 # Docker configurations

## Setup Instructions

### 1. Clone & Setup Environment

# Clone repository
git clone <repository-url>
cd <project-directory>

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

### 2. Environment Configuration

# Generate environment variables
python generate_key.py

### 3. Docker Services

# Start required services
docker-compose up -d

### 4. Django Setup

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver

## API Endpoints

### Customer Portal (CP)
- POST /api/v1/cp/auth/register
- POST /api/v1/cp/auth/login

### CRM
- GET    /api/v1/crm/customers/
- POST   /api/v1/crm/customers/
- GET    /api/v1/crm/customers/{id}/

## Environment Variables

Required variables in `.env`:

# Django
DJANGO_ENV=development
SECRET_KEY=your-secret-key
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

## Development Commands

# Run tests
python manage.py test

# Create new app
python manage.py startapp app_name

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

## Docker Services

The project includes:
- PostgreSQL (Database)
- Redis (Caching)
- Elasticsearch (Search Engine)
- Kibana (Visualization)
- RabbitMQ (Message Queue)

Start all services:
docker-compose up -d

Stop all services:
docker-compose down

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Core Configuration

The `core` module serves as the central configuration hub for the entire project.

### Settings Structure
- `base.py`: Base settings shared across all environments
- `development.py`: Development-specific settings
- `crm.py`: CRM module specific settings
- `cp.py`: Customer Portal specific settings

### Key Components:


### Key Components

1. **Settings Management**
   - Environment-based configuration (development/staging/production)
   - Module-specific settings (CRM/CP)
   - Centralized constants and configurations

2. **Database Integration**
   - PostgreSQL async connection pool
   - SQLAlchemy integration for async operations
   - Connection management and timeout handling

3. **Caching & Redis**
   - Custom Redis cache implementation
   - Rate limiting functionality
   - WebSocket channel layers
   - Session management

4. **Elasticsearch Integration**
   - Custom index mappings and analyzers
   - Environment-specific index prefixing
   - Automatic document mapping
   - Search optimization settings

5. **WebSocket Support**
   - ASGI configuration
   - Separate consumers for:
     - Customer real-time updates
     - Staff notifications
     - System broadcasts

6. **Authentication & Security**
   - JWT token management
   - Rate limiting middleware
   - CORS configuration
   - Audit logging

### Environment-Specific Settings

#### Development Environment
DEBUG=TRUE
ALLOWED_HOSTS=[*]
ELASTICSEARCH_INDEX_PREFIX=dev


### System Constants

1. **Log Events**
   - Customer registration
   - Login attempts
   - Password changes
   - Verification events

2. **Resource Types**
   - Customer
   - Account
   - Transaction
   - Document

3. **Action Types**
   - Create
   - Update
   - Delete
   - Change

### API Endpoints

Base URL structure:
- Customer Portal: `/api/v1/cp/`
- CRM: `/api/v1/crm/`
- Admin: `/admin/`

### WebSocket Routes

- Customer Updates: `ws/customer/{customer_id}/`
- Staff Updates: `ws/staff/{staff_id}/`
- Notifications: `ws/notifications/`

### Integration Settings

1. **Redis Configuration**
   - Connection pooling
   - Timeout handling
   - Rate limiting storage
   - Cache management

2. **Elasticsearch Settings**
   - Custom analyzers
   - Search optimization
   - Index management
   - Document mapping

For detailed configuration options, refer to the respective settings files in the `core/settings/` directory.