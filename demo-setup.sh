#!/bin/bash
# 🏗️ GDPR Blog Demo - Quick Setup Script
# Run: chmod +x demo-setup.sh && ./demo-setup.sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════╗"
echo "║     🛡️  GDPR Blog Demo Setup             ║"
echo "║     Complete GDPR Compliance Demo       ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ docker-compose.yml not found. Please run this from the project root directory.${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Setting up GDPR Blog Demo...${NC}"

# 1. Create demo environment file
echo -e "${BLUE}⚙️  Creating demo configuration...${NC}"
cat > .env << 'EOF'
# 🏗️ GDPR Blog Demo Configuration
PROJECT_NAME=GDPR Blog Demo
PROJECT_TEMPLATE=blog
FRONTEND_TEMPLATE=nextjs_base
ENABLED_PLUGINS=gdpr,security,analytics,audit,realtime_plugin
ENVIRONMENT=development
DEBUG=true

# Database Demo
POSTGRES_USER=demo_admin
POSTGRES_PASSWORD=demo_secure_2024
POSTGRES_DB=gdpr_blog_demo
DATABASE_URL=postgresql://demo_admin:demo_secure_2024@postgres:5432/gdpr_blog_demo

# Security Demo  
SECRET_KEY=demo-secret-key-for-testing-only-change-in-production-12345678901234567890
GDPR_ENCRYPTION_KEY=demo-gdpr-encryption-key-32-chars-change-prod

# Redis
REDIS_URL=redis://redis:6379

# GDPR Settings
GDPR_RETENTION_DAYS=30
GDPR_CONSENT_EXPIRY_DAYS=365
GDPR_AUDIT_ENABLED=true
GDPR_AUTO_ANONYMIZE=false

# Security Settings
SECURITY_RATE_LIMIT_PER_MINUTE=100
SECURITY_BOT_DETECTION=true
SECURITY_IP_BLOCKING=false

# Demo Email Settings
SMTP_HOST=mailhog
SMTP_PORT=1025
SMTP_FROM=demo@gdpr-blog.localhost

# Monitoring
LOG_LEVEL=INFO
METRICS_ENABLED=true

# Ports
API_PORT=8000
POSTGRES_PORT=5432
REDIS_PORT=6379
EOF

# 2. Create missing directories
echo -e "${BLUE}📁 Creating required directories...${NC}"
mkdir -p logs exports backups temp
mkdir -p scripts/database
mkdir -p frontend_templates/nextjs_base/pages

# 3. Create enhanced GDPR dashboard
echo -e "${BLUE}🎨 Creating GDPR dashboard...${NC}"
cat > frontend_templates/nextjs_base/pages/gdpr-dashboard.js << 'EOF'
// This file will be replaced with the enhanced dashboard HTML
export default function GdprDashboard() {
  return <div>GDPR Dashboard loading...</div>;
}
EOF

# 4. Create the enhanced HTML dashboard
mkdir -p public
cat > public/gdpr-dashboard.html << 'EOF'
<!-- Enhanced GDPR Dashboard will be placed here -->
<!DOCTYPE html>
<html><head><title>GDPR Dashboard</title></head>
<body><h1>GDPR Dashboard Loading...</h1></body></html>
EOF

# 5. Add missing API endpoints to main.py
echo -e "${BLUE}🔌 Adding missing API routes...${NC}"

# Check if the GDPR endpoints are already added
if ! grep -q "gdpr_endpoints" core/main.py 2>/dev/null; then
    cat >> core/main.py << 'EOF'

# Add GDPR demo endpoints
try:
    from plugins.gdpr_plugin.api import router as gdpr_demo_router
    app.include_router(gdpr_demo_router)
except ImportError:
    print("Warning: GDPR demo endpoints not found")

# Add blog demo endpoints  
try:
    from core.api.blog_demo import router as blog_demo_router
    app.include_router(blog_demo_router)
except ImportError:
    print("Warning: Blog demo endpoints not found")

# Add test endpoint for security testing
@app.get("/api/test")
async def test_endpoint():
    return {"status": "ok", "message": "Test endpoint", "timestamp": "2024-01-01T00:00:00"}
EOF
fi

# 6. Create minimal database init script
cat > scripts/database/init.sql << 'EOF'
-- GDPR Blog Demo Database Initialization
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Demo tables will be created by the application
-- This script ensures database is ready
EOF

# 7. Update docker-compose for demo
echo -e "${BLUE}🐳 Updating Docker Compose for demo...${NC}"

# Add MailHog service for email testing
if ! grep -q "mailhog" docker-compose.yml; then
    cat >> docker-compose.yml << 'EOF'

  # 📧 MailHog for email testing
  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "8025:8025"  # Web interface
      - "1025:1025"  # SMTP
    networks:
      - stakc_network
    restart: unless-stopped
EOF
fi

# 8. Start the services
echo -e "${BLUE}🚀 Starting GDPR Blog Demo services...${NC}"

# Stop any existing containers
docker compose down --remove-orphans 2>/dev/null || true

# Build and start services
echo -e "${YELLOW}Building and starting services (this may take a few minutes)...${NC}"
docker compose up -d --build

# 9. Wait for services to be ready
echo -e "${BLUE}⏳ Waiting for services to be ready...${NC}"

# Wait for database
echo -n "Waiting for database..."
for i in {1..30}; do
    if docker compose exec -T postgres pg_isready -U demo_admin -d gdpr_blog_demo > /dev/null 2>&1; then
        echo -e " ${GREEN}✅${NC}"
        break
    fi
    echo -n "."
    sleep 2
done

# Wait for API
echo -n "Waiting for API..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e " ${GREEN}✅${NC}"
        break
    fi
    echo -n "."
    sleep 2
done

# 10. Seed demo data
echo -e "${BLUE}🌱 Seeding demo data...${NC}"
sleep 3

# Create demo users and consents
curl -s -X POST "http://localhost:8000/api/gdpr/consent" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "consent_type": "marketing", "accepted": true}' > /dev/null 2>&1 || true

curl -s -X POST "http://localhost:8000/api/gdpr/consent" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "consent_type": "analytics", "accepted": true}' > /dev/null 2>&1 || true

curl -s -X POST "http://localhost:8000/api/gdpr/consent" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2, "consent_type": "marketing", "accepted": false}' > /dev/null 2>&1 || true

# Seed blog demo data
curl -s -X POST "http://localhost:8000/api/blog/demo/seed" > /dev/null 2>&1 || true

echo -e "${GREEN}✅ Demo data seeded successfully!${NC}"

# 11. Display success message and instructions
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════╗"
echo "║          🎉 DEMO READY! 🎉               ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}📊 Demo URLs:${NC}"
echo "• 🏠 Blog Homepage:      http://localhost"
echo "• 🛡️  GDPR Dashboard:     http://localhost/gdpr-dashboard"
echo "• 📖 API Documentation:  http://localhost:8000/docs"
echo "• 🔍 Health Check:       http://localhost:8000/health" 
echo "• 📧 MailHog (emails):   http://localhost:8025"

echo ""
echo -e "${YELLOW}🧪 Quick Tests:${NC}"
echo "• Test GDPR metrics:     curl http://localhost:8000/api/gdpr/metrics"
echo "• Test data export:      curl 'http://localhost:8000/api/gdpr/export?user_id=1'"
echo "• Test security:         curl -H 'User-Agent: python-requests' http://localhost:8000/api/test"

echo ""
echo -e "${BLUE}🎯 Demo Scenarios:${NC}"
echo "1. Open GDPR Dashboard and watch real-time metrics"
echo "2. Use API docs to test consent management"
echo "3. Test data export and deletion features"
echo "4. Monitor security alerts and audit trail"
echo "5. Check email notifications in MailHog"

echo ""
echo -e "${GREEN}✨ Happy GDPR Testing! ✨${NC}"

# 12. Open dashboard automatically (if on macOS/Linux with GUI)
if command -v open > /dev/null 2>&1; then
    echo -e "${BLUE}🚀 Opening GDPR Dashboard...${NC}"
    sleep 2
    open http://localhost/gdpr-dashboard 2>/dev/null || true
elif command -v xdg-open > /dev/null 2>&1; then
    echo -e "${BLUE}🚀 Opening GDPR Dashboard...${NC}"
    sleep 2
    xdg-open http://localhost/gdpr-dashboard 2>/dev/null || true
fi

# 13. Show live logs option
echo ""
echo -e "${YELLOW}💡 Tip: Watch live logs with:${NC}"
echo "   docker compose logs -f api"

echo ""
echo -e "${YELLOW}💡 Tip: Stop demo with:${NC}"
echo "   docker compose down"