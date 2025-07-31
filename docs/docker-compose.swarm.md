# docker-compose.swarm.yml (Swarm Compose file)

This file defines the services, secrets, volumes, and networks for deploying the GDPR-compliant stack in Docker Swarm mode. It uses Docker secrets for sensitive data and sets replica, placement, and healthcheck policies for production resilience.

## Services

- **api**: FastAPI backend, plugin system, read-only filesystem, tmpfs for logs, Swarm secrets, healthcheck, 3 replicas
- **postgres**: PostgreSQL 15, GDPR-compliant logging, custom init script, 1 replica
- **redis**: Redis 7, persistent data, memory limits, LRU policy, 1 replica
- **caddy**: Caddy reverse proxy, frontend static files, HTTPS support, 2 replicas
- **worker**: Celery background tasks, plugin support, Swarm secrets, 2 replicas
- **scheduler**: Celery Beat scheduled tasks, Swarm secrets, 1 replica

## Secrets

- `db_url`, `secret_key`, `gdpr_key`: Managed via Docker secrets for secure injection

## Volumes

- Persistent data for PostgreSQL, Redis, Caddy, GDPR exports, audit logs

## Networks

- Isolated bridge network for all services

---

```dockercompose
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "${API_PORT:-8000}:8000"
    environment:
      - DATABASE_URL_FILE=/run/secrets/db_url
      - SECRET_KEY_FILE=/run/secrets/secret_key
      - GDPR_ENCRYPTION_KEY_FILE=/run/secrets/gdpr_key
      - PROJECT_NAME=${PROJECT_NAME:-STAKC Template}
      - PROJECT_TEMPLATE=${PROJECT_TEMPLATE:-base}
      - ENABLED_PLUGINS=${ENABLED_PLUGINS:-gdpr,security,analytics,audit,data_breach}
      - ENVIRONMENT=${ENVIRONMENT:-production}
    volumes:
      - ./core:/app/core
      - ./plugins:/app/plugins
      - ./project_templates:/app/project_templates
      - gdpr_exports:/app/exports
      - audit_logs:/app/logs
    read_only: true
    tmpfs:
      - /tmp
      - /app/logs
    secrets:
      - db_url
      - secret_key
      - gdpr_key
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
      placement:
        max_replicas_per_node: 1
    depends_on:
      - postgres
      - redis
    networks:
      - stakc_network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

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
    command: >
      postgres
      -c log_statement=all
      -c log_destination=stderr
      -c logging_collector=on
      -c log_directory=/var/log/postgresql
      -c log_filename=postgresql-%Y-%m-%d.log
      -c log_rotation_age=1d
      -c log_rotation_size=100MB
    deploy:
      replicas: 1
      placement:
        max_replicas_per_node: 1

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
    deploy:
      replicas: 1
      placement:
        max_replicas_per_node: 1

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
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure

  worker:
    build:
      context: .
      dockerfile: Dockerfile
    command: celery -A core.celery worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-admin}:${POSTGRES_PASSWORD:-secure123}@postgres:5432/${POSTGRES_DB:-stakc_app}
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY_FILE=/run/secrets/secret_key
      - GDPR_ENCRYPTION_KEY_FILE=/run/secrets/gdpr_key
      - ENABLED_PLUGINS=${ENABLED_PLUGINS:-gdpr,security,analytics,audit,data_breach}
    volumes:
      - ./core:/app/core
      - ./plugins:/app/plugins
      - gdpr_exports:/app/exports
      - audit_logs:/app/logs
    secrets:
      - secret_key
      - gdpr_key
    depends_on:
      - postgres
      - redis
    networks:
      - stakc_network
    restart: unless-stopped
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure

  scheduler:
    build:
      context: .
      dockerfile: Dockerfile
    command: celery -A core.celery beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER:-admin}:${POSTGRES_PASSWORD:-secure123}@postgres:5432/${POSTGRES_DB:-stakc_app}
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY_FILE=/run/secrets/secret_key
      - GDPR_ENCRYPTION_KEY_FILE=/run/secrets/gdpr_key
      - ENABLED_PLUGINS=${ENABLED_PLUGINS:-gdpr,security,analytics,audit,data_breach}
    volumes:
      - ./core:/app/core
      - ./plugins:/app/plugins
    secrets:
      - secret_key
      - gdpr_key
    depends_on:
      - postgres
      - redis
    networks:
      - stakc_network
    restart: unless-stopped
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure

secrets:
  db_url:
    file: .secrets/db_url
  secret_key:
    file: .secrets/secret_key
  gdpr_key:
    file: .secrets/gdpr_key

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  caddy_data:
    driver: local
  caddy_config:
    driver: local
  gdpr_exports:
    driver: local
  audit_logs:
    driver: local

networks:
  stakc_network:
    driver: bridge
```
