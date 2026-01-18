# DevOps Project: Flask + Nginx + PostgreSQL with Docker

## Project Overview
Complete DevOps environment for a Flask web application with PostgreSQL database and Nginx reverse proxy, featuring multi-stage Docker builds, automated testing, database seeding, and CI/CD pipelines.

## Architecture
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Nginx │────▶│ Flask │────▶│ PostgreSQL │
│ (reverse │ │ (Python) │ │ (Database) │
│ proxy) │◀────│ │◀────│ │
└─────────────┘ └─────────────┘ └─────────────┘
│ │ │
front_net both nets back_net

## Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Git
- Azure CLI (for IaC deployment)

## Quick Start

### 1. Clone and build
```bash
git clone <repository-url>
cd devops-project
docker-compose up --build
```

### 2. Access the application
API: http://localhost:8080/api/health

### 3. Check services
```bash
docker-compose ps
docker-compose logs -f
```

## Key Features

### Docker Multi-stage Build
- Builder stage: Installs dependencies and prepares application
- Test stage: Runs pytest with code coverage
- Final stage: Production-optimized image

### Docker Compose Services
- app: Flask application
- nginx: Reverse proxy with logging
- db: PostgreSQL database
- migration_runner: Database migrations
- seed_runner: Database seeding with file export

### CI/CD Pipeline
- CI: Automated testing, security scanning, image building
- CD: Manual/auto deployment with health checks

### Database Management
- Automated migrations with Flask-Migrate
- Seeder with CSV/JSON export
- Volume persistence for data

## Development

### Running tests
```bash
# Using Docker
docker build --target test .

# Locally
cd app
pip install -r requirements.txt
pytest tests/ -v
```

### Database operations
```bash
# Run migrations
docker-compose run --rm migration_runner

# Seed database
docker-compose run --rm seed_runner

# Access database
docker-compose exec db psql -U flask_user -d flask_db
```

### Viewing logs
```bash
# Application logs
docker-compose logs -f app

# Nginx logs
docker-compose logs -f nginx
docker-compose exec nginx tail -f /var/log/nginx/access.log

# Database logs
docker-compose logs -f db
```

## Deployment

### Azure Infrastructure
```bash
cd infra
az deployment group create \
  --resource-group devops-project-rg \
  --template-file main.bicep \
  --parameters parameters.json
```

### Production deployment
1. Push to main branch triggers CI
2. Manually trigger CD pipeline from GitHub Actions
3. Or push version tag: git tag v1.0.0 && git push origin v1.0.0

## Monitoring

### Health checks
curl http://localhost:8080/api/health

### Container status
docker-compose ps
docker stats

### Volume inspection
docker volume ls
docker volume inspect devops-project_db_data

### Reset everything
```bash
docker-compose down -v
docker system prune -af
docker volume prune -f
```

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/users` - List all users
- `POST /api/users` - Create new user
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/:id/complete` - Complete task

## License

### MIT