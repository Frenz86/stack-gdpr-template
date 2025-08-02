#!/bin/bash
# quick-deploy-18.171.217.18.sh - VERSIONE CORRETTA

set -e  # Exit on error

echo "🚀 Quick Deploy per EC2 18.171.217.18"

# Stop services esistenti
echo "🛑 Stopping existing services..."
docker-compose down 2>/dev/null || true
docker-compose -f docker-compose.ec2.yml down 2>/dev/null || true

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
CORS_ORIGINS=http://18.171.217.18,http://18.171.217.18:8000,http://localhost:3000
API_PORT=8000
POSTGRES_PORT=5432
REDIS_PORT=6379
EOF
    echo "✅ .env file created"
fi

# Crea directory necessarie
echo "📁 Creating directories..."
mkdir -p logs exports backups temp public scripts/database

# Rimuovi init.sql se è una directory
if [ -d "scripts/database/init.sql" ]; then
    echo "🔧 Fixing init.sql directory conflict..."
    rm -rf scripts/database/init.sql
fi

# Crea init.sql di base
echo "🗄️ Creating database init script..."
cat > scripts/database/init.sql << 'EOF'
-- STAKC GDPR Template Database Initialization
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create basic tables for GDPR compliance
CREATE TABLE IF NOT EXISTS gdpr_consent_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255),
    consent_type VARCHAR(100),
    consent_given BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT
);

CREATE TABLE IF NOT EXISTS gdpr_data_requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255),
    request_type VARCHAR(50), -- 'export', 'delete', 'update'
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    notes TEXT
);

SELECT 'STAKC GDPR Database Ready' as status;
EOF

# Crea docker-compose.ec2.yml se non esiste
if [ ! -f "docker-compose.ec2.yml" ]; then
    echo "🐳 Creating docker-compose.ec2.yml..."
    cat > docker-compose.ec2.yml << 'EOF'
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "0.0.0.0:8000:8000"
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
      - ./logs:/app/logs
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
    ports:
      - "127.0.0.1:5432:5432"
    networks:
      - stakc_network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "127.0.0.1:6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    networks:
      - stakc_network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  gdpr_exports:

networks:
  stakc_network:
    driver: bridge
EOF
    echo "✅ docker-compose.ec2.yml created"
fi

# Crea index.html di base
echo "🏠 Creating homepage..."
cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>STAKC GDPR Blog - AWS EC2</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            text-align: center; 
            padding: 50px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            margin: 0;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            max-width: 600px;
            margin: 0 auto;
        }
        .btn { 
            display: inline-block;
            padding: 12px 24px; 
            margin: 10px; 
            background: rgba(255,255,255,0.2); 
            color: white; 
            text-decoration: none; 
            border-radius: 8px; 
            border: 1px solid rgba(255,255,255,0.3);
            transition: all 0.3s ease;
        }
        .btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        .status {
            margin: 20px 0;
            padding: 10px;
            background: rgba(0,255,0,0.2);
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ STAKC GDPR Blog</h1>
        <p>Running on AWS EC2: <strong>18.171.217.18</strong></p>
        <div class="status">
            <p>✅ Server is running</p>
        </div>
        <div>
            <a href="/health" class="btn">Health Check</a>
            <a href="/docs" class="btn">API Documentation</a>
            <a href="/api/gdpr/metrics" class="btn">GDPR Metrics</a>
            <a href="/redoc" class="btn">ReDoc</a>
        </div>
        <br>
        <p><small>Powered by STAKC Framework</small></p>
    </div>
</body>
</html>
EOF

# Verifica che Docker sia in esecuzione
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Cleanup vecchie immagini
echo "🧹 Cleaning up old images..."
docker system prune -f

# Build e start
echo "🐳 Building and starting Docker services..."
docker-compose -f docker-compose.ec2.yml up --build -d

# Wait for startup
echo "⏳ Waiting for services to start (90s)..."
for i in {1..18}; do
    echo -n "."
    sleep 5
done
echo ""

# Health checks
echo "🔍 Running health checks..."

# Check interno
echo -n "Internal health check: "
if curl -f -s http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ OK"
else
    echo "❌ FAILED"
fi

# Check esterno
echo -n "External health check: "
if curl -f -s http://18.171.217.18:8000/health >/dev/null 2>&1; then
    echo "✅ OK"
else
    echo "❌ FAILED (check Security Groups)"
fi

# Show status
echo ""
echo "📊 Service status:"
docker compose -f docker-compose.ec2.yml ps

# Show logs se ci sono errori
echo ""
echo "📋 Recent logs:"
docker compose -f docker-compose.ec2.yml logs --tail=10 api

echo ""
echo "🎉 Deploy completed!"
echo ""
echo "🔗 Access URLs:"
echo "   • Health: http://18.171.217.18:8000/health"
echo "   • API Docs: http://18.171.217.18:8000/docs"
echo "   • GDPR Metrics: http://18.171.217.18:8000/api/gdpr/metrics"
echo "   • Homepage: http://18.171.217.18/"
echo ""
echo "🔧 Troubleshooting:"
echo "   • Check logs: docker-compose -f docker-compose.ec2.yml logs api"
echo "   • Restart: docker-compose -f docker-compose.ec2.yml restart"
echo "   • Stop: docker-compose -f docker-compose.ec2.yml down"
echo ""

# Test finale
echo "🧪 Final connectivity test..."
timeout 10 curl -v http://18.171.217.18:8000/health || echo "⚠️  External access may be blocked by Security Groups"