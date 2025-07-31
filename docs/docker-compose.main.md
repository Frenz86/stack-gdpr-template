# docker-compose.yml (Main Compose file)

This file defines the main services, volumes, and networks for the GDPR-compliant stack. It is compatible with both Docker Compose and Swarm (with environment variable secrets).

## Services
- **api**: FastAPI backend, plugin system, read-only filesystem, tmpfs for logs
- **postgres**: PostgreSQL 15, GDPR-compliant logging, automatic backup, custom init script
- **redis**: Redis 7, persistent data, memory limits, LRU policy
- **caddy**: Caddy reverse proxy, frontend static files, HTTPS support
- **worker**: Celery background tasks, plugin support
- **scheduler**: Celery Beat scheduled tasks

## Volumes
- Persistent data for PostgreSQL, Redis, Caddy, GDPR exports, audit logs

## Networks
- Isolated bridge network for all services

## Development Extensions
- Override with `docker-compose.override.yml` for hot-reload, debug, and local mounts

---

```
version: '3.8'

services:
  # 🚀 Backend API
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "${API_PORT:-8000}:8000"
    environment:
      # 🚨 SECURITY: Usa variabili d'ambiente per compatibilità Compose/Swarm
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
      - GDPR_ENCRYPTION_KEY=${GDPR_ENCRYPTION_KEY}
      - PROJECT_NAME=${PROJECT_NAME:-STAKC Template}
      - PROJECT_TEMPLATE=${PROJECT_TEMPLATE:-base}
      - ENABLED_PLUGINS=${ENABLED_PLUGINS:-gdpr,security,analytics,audit,data_breach}
      - ENVIRONMENT=${ENVIRONMENT:-development}
    volumes:
      - ./core:/app/core
      - ./plugins:/app/plugins
      - ./project_templates:/app/project_templates
      - gdpr_exports:/app/exports
      - audit_logs:/app/logs
    # 🚨 SECURITY: Read-only filesystem
    read_only: true
    tmpfs:
      - /tmp
      - /app/logs

  # 🐘 PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-admin}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-secure123}
      POSTGRES_DB: ${POSTGRES_DB:-stakc_app}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/database/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    networks:
      - stakc_network
    restart: unless-stopped
    # GDPR: Backup automatico per compliance
    command: >
      postgres
      -c log_statement=all
      -c log_destination=stderr
      -c logging_collector=on
      -c log_directory=/var/log/postgresql
      -c log_filename=postgresql-%Y-%m-%d.log
      -c log_rotation_age=1d
      -c log_rotation_size=100MB

  # 📦 Redis Cache & Sessions
  redis:
    image: redis:7-alpine
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    networks:
      - stakc_network
    restart: unless-stopped

  # 🌐 Caddy Reverse Proxy
  caddy:
    image: caddy:2-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
      - ./frontend_templates/${FRONTEND_TEMPLATE:-nextjs_base}/dist:/srv/frontend:ro
    environment:
      - DOMAIN=${DOMAIN:-localhost}
      - API_UPSTREAM=api:8000
    networks:
      - stakc_network
    restart: unless-stopped

  # 📊 Celery Worker (Background Tasks)
  worker:
    build:
      context: .
      dockerfile: Dockerfile
    command: celery -A core.celery worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-admin}:${POSTGRES_PASSWORD:-secure123}@postgres:5432/${POSTGRES_DB:-stakc_app}
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY:-your-super-secret-key-change-in-production}
      - GDPR_ENCRYPTION_KEY=${GDPR_ENCRYPTION_KEY:-gdpr-encryption-key-32-chars-min}
      - ENABLED_PLUGINS=${ENABLED_PLUGINS:-gdpr,security,analytics,audit,data_breach}
    volumes:
      - ./core:/app/core
      - ./plugins:/app/plugins
      - gdpr_exports:/app/exports
      - audit_logs:/app/logs
    depends_on:
      - postgres
      - redis
    networks:
      - stakc_network
    restart: unless-stopped

  # ⏰ Celery Beat (Scheduled Tasks)
  scheduler:
    build:
      context: .
      dockerfile: Dockerfile
    command: celery -A core.celery beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-admin}:${POSTGRES_PASSWORD:-secure123}@postgres:5432/${POSTGRES_DB:-stakc_app}
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY:-your-super-secret-key-change-in-production}
      - GDPR_ENCRYPTION_KEY=${GDPR_ENCRYPTION_KEY:-gdpr-encryption-key-32-chars-min}
      - ENABLED_PLUGINS=${ENABLED_PLUGINS:-gdpr,security,analytics,audit,data_breach}
    volumes:
      - ./core:/app/core
      - ./plugins:/app/plugins
    depends_on:
      - postgres
      - redis
    networks:
      - stakc_network
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  caddy_data:
    driver: local
  caddy_config:
    driver: local
  # GDPR Compliance Volumes
  gdpr_exports:
    driver: local
  audit_logs:
    driver: local

networks:
  stakc_network:
    driver: bridge

# 🔧 Development Extensions (override in docker-compose.override.yml)
x-development: &development
  environment:
    - DEBUG=true
    - LOG_LEVEL=DEBUG
  volumes:
    - .:/app
  command: uvicorn core.main:app --host 0.0.0.0 --port 8000 --reload
```
