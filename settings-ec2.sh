# 🔧 Configurazione Specifica per EC2 IP: 18.171.217.18

## 1. Test di Connettività Immediato
```bash
# Da un terminale esterno (tuo computer locale):
curl -I http://18.171.217.18:8000/health
curl -I http://18.171.217.18:80
curl -I http://18.171.217.18/health

# Se non risponde, il problema è Security Groups o Docker binding
```

## 2. File .env Ottimizzato per questo IP
```env
# .env per EC2 18.171.217.18
PROJECT_NAME=my-blog
PROJECT_TEMPLATE=blog
FRONTEND_TEMPLATE=nextjs_base
ENABLED_PLUGINS=gdpr,security,analytics,audit
ENVIRONMENT=production

# Domain/IP specifico
DOMAIN=18.171.217.18
API_URL=http://18.171.217.18:8000

# Database
POSTGRES_USER=admin
POSTGRES_PASSWORD=secure_blog_2024_aws
POSTGRES_DB=stakc_app
DATABASE_URL=postgresql://admin:secure_blog_2024_aws@postgres:5432/stakc_app

# Redis
REDIS_URL=redis://redis:6379

# Security Keys - CAMBIA QUESTI!
SECRET_KEY=aws-ec2-secret-key-for-stakc-blog-2024-change-this-in-prod-67890
GDPR_ENCRYPTION_KEY=gdpr-encryption-key-aws-ec2-change

# Logging
LOG_LEVEL=INFO
DEBUG=false

# CORS per permettere accesso dall'IP pubblico
CORS_ORIGINS=http://18.171.217.18,http://18.171.217.18:8000,http://localhost:3000

# Porte
API_PORT=8000
POSTGRES_PORT=5432
REDIS_PORT=6379
```

## 3. docker-compose.ec2.yml per il tuo IP
```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "0.0.0.0:8000:8000"  # CRITICO: bind su tutte le interfacce
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
      - GDPR_ENCRYPTION_KEY=${GDPR_ENCRYPTION_KEY}
      - PROJECT_NAME=${PROJECT_NAME:-my-blog}
      - PROJECT_TEMPLATE=${PROJECT_TEMPLATE:-blog}
      - ENABLED_PLUGINS=${ENABLED_PLUGINS:-gdpr,security,analytics,audit}
      - ENVIRONMENT=production
      - CORS_ORIGINS=http://18.171.217.18,http://18.171.217.18:8000
    volumes:
      - ./core:/app/core
      - ./plugins:/app/plugins
      - ./project_templates:/app/project_templates
      - gdpr_exports:/app/exports
    tmpfs:
      - /tmp
      - /app/logs
    depends_on:
      - postgres
      - redis
    networks:
      - stakc_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-admin}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-secure_blog_2024_aws}
      POSTGRES_DB: ${POSTGRES_DB:-stakc_app}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/database/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    # Solo localhost per sicurezza
    ports:
      - "127.0.0.1:5432:5432"
    networks:
      - stakc_network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    # Solo localhost per sicurezza
    ports:
      - "127.0.0.1:6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    networks:
      - stakc_network
    restart: unless-stopped

  caddy:
    image: caddy:2-alpine
    ports:
      - "0.0.0.0:80:80"
      - "0.0.0.0:443:443"
    volumes:
      - ./Caddyfile.ec2:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
      - ./public:/srv/public:ro
    environment:
      - DOMAIN=18.171.217.18
      - API_UPSTREAM=api:8000
    networks:
      - stakc_network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  caddy_data:
  caddy_config:
  gdpr_exports:

networks:
  stakc_network:
    driver: bridge
```

## 4. Caddyfile.ec2 per il tuo IP
```caddy
{
    admin off
    email admin@18.171.217.18
}

# Configurazione per IP pubblico AWS
18.171.217.18:80 {
    encode gzip
    
    # Security headers
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "no-referrer"
        Access-Control-Allow-Origin "http://18.171.217.18"
    }
    
    # API routes
    reverse_proxy /api/* api:8000
    reverse_proxy /docs* api:8000
    reverse_proxy /redoc* api:8000
    reverse_proxy /openapi.json api:8000
    reverse_proxy /health api:8000
    
    # Root endpoint
    reverse_proxy / api:8000
    
    # Error handling
    handle_errors {
        respond "{http.error.status_code} {http.error.status_text}" 500
    }
}
```

## 5. Script di Deploy Rapido
```bash
#!/bin/bash
# quick-deploy-18.171.217.18.sh

echo "🚀 Quick Deploy per EC2 18.171.217.18"

# Stop services
docker-compose down 2>/dev/null

# Crea .env se non esiste
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
PROJECT_NAME=my-blog
PROJECT_TEMPLATE=blog
FRONTEND_TEMPLATE=nextjs_base
ENABLED_PLUGINS=gdpr,security,analytics,audit
ENVIRONMENT=production
DOMAIN=18.171.217.18
API_URL=http://18.171.217.18:8000
POSTGRES_USER=admin
POSTGRES_PASSWORD=secure_blog_2024_aws
POSTGRES_DB=stakc_app
DATABASE_URL=postgresql://admin:secure_blog_2024_aws@postgres:5432/stakc_app
REDIS_URL=redis://redis:6379
SECRET_KEY=aws-ec2-secret-key-for-stakc-blog-2024-change-this-in-prod-67890
GDPR_ENCRYPTION_KEY=gdpr-encryption-key-aws-ec2-change
LOG_LEVEL=INFO
DEBUG=false
CORS_ORIGINS=http://18.171.217.18,http://18.171.217.18:8000
API_PORT=8000
POSTGRES_PORT=5432
REDIS_PORT=6379
EOF
fi

# Crea directory se non esistono
mkdir -p logs exports backups temp public scripts/database

# Crea init.sql di base
cat > scripts/database/init.sql << 'EOF'
-- STAKC GDPR Template Database Initialization
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
SELECT 'STAKC GDPR Database Ready' as status;
EOF

# Crea index.html di base
cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>STAKC GDPR Blog - AWS EC2</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        .btn { padding: 10px 20px; margin: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🛡️ STAKC GDPR Blog</h1>
    <p>Running on AWS EC2: 18.171.217.18</p>
    <div>
        <a href="/health" class="btn">Health Check</a>
        <a href="/docs" class="btn">API Docs</a>
        <a href="/api/gdpr/metrics" class="btn">GDPR Metrics</a>
    </div>
</body>
</html>
EOF

# Build e start
echo "🐳 Starting Docker services..."
docker-compose -f docker-compose.ec2.yml up --build -d

# Wait for startup
echo "⏳ Waiting for services (60s)..."
sleep 60

# Health checks
echo "🔍 Running health checks..."
echo "Local health check:"
curl -f http://localhost:8000/health && echo " ✅" || echo " ❌"

echo "External health check:"
curl -f http://18.171.217.18:8000/health && echo " ✅" || echo " ❌"

# Show status
echo "📊 Service status:"
docker-compose -f docker-compose.ec2.yml ps

echo ""
echo "🎉 Deploy completed!"
echo "🔗 Access URLs:"
echo "   • Health: http://18.171.217.18:8000/health"
echo "   • API Docs: http://18.171.217.18:8000/docs"
echo "   • GDPR Metrics: http://18.171.217.18:8000/api/gdpr/metrics"
echo "   • Homepage: http://18.171.217.18/"
```

## 6. Test di Connettività Specifico
```bash
#!/bin/bash
# test-18.171.217.18.sh

echo "🧪 Testing connectivity to 18.171.217.18"

# Test porte aperte
echo "🔌 Port scanning..."
nmap -p 80,8000,443 18.171.217.18

# Test HTTP endpoints
echo "🌐 HTTP endpoint tests..."
curl -I http://18.171.217.18:8000/health
curl -I http://18.171.217.18:80/
curl -I http://18.171.217.18/docs

# Test with verbose output
echo "🔍 Detailed health check..."
curl -v http://18.171.217.18:8000/health

echo "✅ Tests completed"
```