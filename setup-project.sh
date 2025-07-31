#!/bin/bash

# 🏗️ STAKC GDPR Template - Setup Nuovo Progetto
# Versione: 2.0.0
# Autore: STAKC Team

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
PROJECT_NAME=""
PROJECT_TEMPLATE="base"
PLUGINS="gdpr,security"
FRONTEND="nextjs_base"
DOMAIN="localhost"
ENVIRONMENT="development"

# Print banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════╗"
echo "║        🏗️  STAKC GDPR TEMPLATE          ║"
echo "║      Setup Nuovo Progetto v2.0.0        ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${NC}"

# Help function
show_help() {
    echo "Usage: $0 --name=PROJECT_NAME [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --name=NAME              Nome del progetto (obbligatorio)"
    echo "  --template=TEMPLATE      Template progetto [base|blog|ecommerce|crm|document_management]"
    echo "  --plugins=PLUGINS        Plugin da attivare (comma-separated) [gdpr,security,analytics,notifications]"
    echo "  --frontend=FRONTEND      Template frontend [nextjs_base|react_admin|vue_spa|vanilla_html]"
    echo "  --domain=DOMAIN          Dominio per deployment [localhost]"
    echo "  --env=ENVIRONMENT        Environment [development|staging|production]"
    echo "  --help                   Mostra questo help"
    echo ""
    echo "Esempi:"
    echo "  $0 --name=my-blog --template=blog --plugins=gdpr,security"
    echo "  $0 --name=my-shop --template=ecommerce --plugins=gdpr,security,analytics"
    echo "  $0 --name=my-docs --template=document_management --frontend=react_admin"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --name=*)
            PROJECT_NAME="${1#*=}"
            shift
            ;;
        --template=*)
            PROJECT_TEMPLATE="${1#*=}"
            shift
            ;;
        --plugins=*)
            PLUGINS="${1#*=}"
            shift
            ;;
        --frontend=*)
            FRONTEND="${1#*=}"
            shift
            ;;
        --domain=*)
            DOMAIN="${1#*=}"
            shift
            ;;
        --env=*)
            ENVIRONMENT="${1#*=}"
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Parametro sconosciuto: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Validate required parameters
if [ -z "$PROJECT_NAME" ]; then
    echo -e "${RED}❌ Nome progetto obbligatorio! Usa --name=nome_progetto${NC}"
    show_help
    exit 1
fi

# Validate template
AVAILABLE_TEMPLATES=("base" "blog" "ecommerce" "crm" "document_management")
if [[ ! " ${AVAILABLE_TEMPLATES[@]} " =~ " ${PROJECT_TEMPLATE} " ]]; then
    echo -e "${RED}❌ Template non valido: $PROJECT_TEMPLATE${NC}"
    echo -e "${YELLOW}Template disponibili: ${AVAILABLE_TEMPLATES[*]}${NC}"
    exit 1
fi

# Validate frontend
AVAILABLE_FRONTENDS=("nextjs_base" "react_admin" "vue_spa" "vanilla_html")
if [[ ! " ${AVAILABLE_FRONTENDS[@]} " =~ " ${FRONTEND} " ]]; then
    echo -e "${RED}❌ Frontend non valido: $FRONTEND${NC}"
    echo -e "${YELLOW}Frontend disponibili: ${AVAILABLE_FRONTENDS[*]}${NC}"
    exit 1
fi

echo -e "${GREEN}🚀 Configurazione progetto:${NC}"
echo -e "   📁 Nome: ${BLUE}$PROJECT_NAME${NC}"
echo -e "   📋 Template: ${BLUE}$PROJECT_TEMPLATE${NC}"
echo -e "   🔌 Plugin: ${BLUE}$PLUGINS${NC}"
echo -e "   🎨 Frontend: ${BLUE}$FRONTEND${NC}"
echo -e "   🌐 Dominio: ${BLUE}$DOMAIN${NC}"
echo -e "   🏷️  Environment: ${BLUE}$ENVIRONMENT${NC}"
echo ""

# Confirm setup
read -p "Continuare con il setup? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⏹️  Setup annullato${NC}"
    exit 0
fi

PROJECT_DIR="../$PROJECT_NAME"

# Check if project directory already exists
if [ -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Directory $PROJECT_DIR già esistente!${NC}"
    read -p "Sovrascrivere? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$PROJECT_DIR"
        echo -e "${YELLOW}🗑️  Directory esistente rimossa${NC}"
    else
        exit 1
    fi
fi

echo -e "${BLUE}📂 Creazione directory progetto...${NC}"
mkdir -p "$PROJECT_DIR"
cd "$(dirname "$0")/.."

# Copy base template
echo -e "${BLUE}📋 Copia template base...${NC}"
cp -r . "$PROJECT_DIR/"
cd "$PROJECT_DIR"

# Remove template-specific files
rm -rf examples/
rm -rf docs/
rm -f setup-project.sh

# Copy Caddyfile template
cp Caddyfile.template Caddyfile

# Generate .env file
echo -e "${BLUE}⚙️  Generazione configurazione...${NC}"
cat > .env << EOF
# 🏗️ STAKC GDPR Template - $PROJECT_NAME
# Generated: $(date)

# Project Configuration
PROJECT_NAME="$PROJECT_NAME"
PROJECT_TEMPLATE="$PROJECT_TEMPLATE"
FRONTEND_TEMPLATE="$FRONTEND"
ENABLED_PLUGINS="$PLUGINS"
ENVIRONMENT="$ENVIRONMENT"

# Domain & URLs
DOMAIN="$DOMAIN"
API_PORT=8000
POSTGRES_PORT=$(shuf -i 5433-5499 -n 1)
REDIS_PORT=$(shuf -i 6380-6399 -n 1)

# Database
POSTGRES_USER="admin"
POSTGRES_PASSWORD="$(openssl rand -base64 32 | tr -d '/')"
POSTGRES_DB="${PROJECT_NAME//-/_}_db"

# Security
SECRET_KEY="$(openssl rand -base64 64 | tr -d '/')"
GDPR_ENCRYPTION_KEY="$(openssl rand -base64 32 | tr -d '/')"

# GDPR Settings
GDPR_RETENTION_DAYS=1095
GDPR_CONSENT_EXPIRY_DAYS=365
GDPR_AUDIT_ENABLED=true

# Security Settings  
SECURITY_RATE_LIMIT_PER_MINUTE=60
SECURITY_BOT_DETECTION=true
SECURITY_IP_BLOCKING=true

# Email (configure for production)
SMTP_HOST="localhost"
SMTP_PORT=1025
SMTP_USER=""
SMTP_PASSWORD=""
SMTP_FROM="noreply@$DOMAIN"

# Monitoring
LOG_LEVEL="INFO"
METRICS_ENABLED=true
EOF

# Generate docker-compose.override.yml for development
if [ "$ENVIRONMENT" = "development" ]; then
    echo -e "${BLUE}🔧 Setup environment di sviluppo...${NC}"
    cat > docker-compose.override.yml << EOF
version: '3.8'

services:
  api:
    <<: *development
    ports:
      - "\${API_PORT:-8000}:8000"
    
  postgres:
    ports:
      - "\${POSTGRES_PORT:-5432}:5432"
      
  redis:
    ports:
      - "\${REDIS_PORT:-6379}:6379"

# Development tools
  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "8025:8025"  # Web interface
      - "1025:1025"  # SMTP
    networks:
      - stakc_network
EOF
fi

# Setup project-specific template
if [ "$PROJECT_TEMPLATE" != "base" ]; then
    echo -e "${BLUE}📋 Setup template specifico: $PROJECT_TEMPLATE...${NC}"
    
    if [ -d "project_templates/$PROJECT_TEMPLATE" ]; then
        # Copy project-specific files to core
        cp -r project_templates/$PROJECT_TEMPLATE/* core/
        echo -e "${GREEN}✅ Template $PROJECT_TEMPLATE applicato${NC}"
    else
        echo -e "${YELLOW}⚠️  Template $PROJECT_TEMPLATE non trovato, usando base${NC}"
    fi
fi

# Setup frontend
echo -e "${BLUE}🎨 Setup frontend: $FRONTEND...${NC}"
if [ -d "frontend_templates/$FRONTEND" ]; then
    cd frontend_templates/$FRONTEND
    
    case $FRONTEND in
        "nextjs_base")
            echo -e "${BLUE}📦 Installazione dipendenze Next.js...${NC}"
            if command -v npm &> /dev/null; then
                npm install
                npm run build
            else
                echo -e "${YELLOW}⚠️  npm non trovato, installa manualmente con: cd frontend_templates/$FRONTEND && npm install${NC}"
            fi
            ;;
        "react_admin")
            echo -e "${BLUE}📦 Installazione dipendenze React Admin...${NC}"
            if command -v npm &> /dev/null; then
                npm install
                npm run build
            fi
            ;;
    esac
    
    cd ../..
    echo -e "${GREEN}✅ Frontend $FRONTEND configurato${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend $FRONTEND non trovato${NC}"
fi

# Generate plugin-specific configuration
echo -e "${BLUE}🔌 Configurazione plugin...${NC}"
IFS=',' read -ra PLUGIN_ARRAY <<< "$PLUGINS"
for plugin in "${PLUGIN_ARRAY[@]}"; do
    plugin=$(echo "$plugin" | xargs) # trim whitespace
    
    case $plugin in
        "gdpr")
            echo -e "${GREEN}🛡️  Plugin GDPR attivato${NC}"
            # Copy GDPR-specific config
            if [ -f "config/plugin_configs/gdpr.yml" ]; then
                sed "s/PROJECT_NAME_PLACEHOLDER/$PROJECT_NAME/g" config/plugin_configs/gdpr.yml > config/gdpr_active.yml
            fi
            ;;
        "security")
            echo -e "${GREEN}🔒 Plugin Security attivato${NC}"
            ;;
        "analytics")
            echo -e "${GREEN}📊 Plugin Analytics attivato${NC}"
            ;;
        "notifications")
            echo -e "${GREEN}📧 Plugin Notifications attivato${NC}"
            ;;
        *)
            echo -e "${YELLOW}⚠️  Plugin sconosciuto: $plugin${NC}"
            ;;
    esac
done

# Initialize database
mkdir -p scripts/database
echo -e "${BLUE}🗄️  Preparazione database...${NC}"
cat > scripts/database/init.sql << EOF
-- STAKC GDPR Template Database Initialization
-- Project: $PROJECT_NAME
-- Generated: $(date)

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create application user
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${PROJECT_NAME//-/_}_app') THEN
        CREATE ROLE ${PROJECT_NAME//-/_}_app WITH LOGIN PASSWORD '$(openssl rand -base64 16)';
    END IF;
END
\$\$;

-- Grant permissions
GRANT CONNECT ON DATABASE ${PROJECT_NAME//-/_}_db TO ${PROJECT_NAME//-/_}_app;
GRANT USAGE ON SCHEMA public TO ${PROJECT_NAME//-/_}_app;
GRANT CREATE ON SCHEMA public TO ${PROJECT_NAME//-/_}_app;

-- Create basic audit function for GDPR compliance
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS \$audit\$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit_logs (table_name, operation, old_data, timestamp, user_id)
        VALUES (TG_TABLE_NAME, TG_OP, row_to_json(OLD), CURRENT_TIMESTAMP, current_setting('app.current_user_id', true));
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_logs (table_name, operation, old_data, new_data, timestamp, user_id)
        VALUES (TG_TABLE_NAME, TG_OP, row_to_json(OLD), row_to_json(NEW), CURRENT_TIMESTAMP, current_setting('app.current_user_id', true));
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit_logs (table_name, operation, new_data, timestamp, user_id)
        VALUES (TG_TABLE_NAME, TG_OP, row_to_json(NEW), CURRENT_TIMESTAMP, current_setting('app.current_user_id', true));
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
\$audit\$ LANGUAGE plpgsql;
EOF

# Generate README for the project
echo -e "${BLUE}📚 Generazione documentazione...${NC}"
cat > README.md << EOF
# $PROJECT_NAME

**Template**: $PROJECT_TEMPLATE  
**Frontend**: $FRONTEND  
**Plugin Attivi**: $PLUGINS  
**Environment**: $ENVIRONMENT  

Progetto generato da STAKC GDPR Template v2.0.0

## 🚀 Quick Start

\`\`\`bash
# Avvia il progetto
docker compose up -d

# Controlla i logs
docker compose logs -f api

# Accedi all'applicazione
open http://$DOMAIN
\`\`\`

## 🔌 Plugin Attivi

$(for plugin in $(echo $PLUGINS | tr ',' ' '); do
    case $plugin in
        "gdpr") echo "- **🛡️ GDPR Plugin**: Compliance automatica, export dati, gestione consensi" ;;
        "security") echo "- **🔒 Security Plugin**: Rate limiting, bot detection, audit sicurezza" ;;
        "analytics") echo "- **📊 Analytics Plugin**: Metriche e monitoring" ;;
        "notifications") echo "- **📧 Notifications Plugin**: Email, SMS, Slack notifications" ;;
    esac
done)

## 🛡️ GDPR Compliance

Questo progetto è **automaticamente GDPR-compliant** grazie al plugin integrato:

- ✅ Gestione consensi automatica
- ✅ Export dati utente (Right to Data Portability)
- ✅ Cancellazione dati (Right to Erasure)
- ✅ Audit trail completo
- ✅ Crittografia dati sensibili
- ✅ Cookie management
- ✅ Privacy policy auto-generata

### API Endpoints GDPR:
- \`GET /api/gdpr/my-data\` - Export dati utente
- \`DELETE /api/gdpr/delete-account\` - Cancellazione account
- \`POST /api/gdpr/consent\` - Gestione consensi
- \`GET /api/gdpr/audit-logs\` - Log delle operazioni

## 🔧 Configurazione

Modifica il file \`.env\` per personalizzare:

\`\`\`bash
# Database
POSTGRES_PASSWORD=password

# Security
SECRET_KEY=secret
GDPR_ENCRYPTION_KEY=encription

# Email
SMTP_HOST=your-smtp-host
SMTP_USER=your-smtp-user
SMTP_PASSWORD=smtp-password
\`\`\`

## 📊 Monitoring

- **Health Check**: http://$DOMAIN/health
- **API Docs**: http://$DOMAIN/docs
- **Admin Panel**: http://$DOMAIN/admin
- **MailHog** (dev): http://$DOMAIN:8025

## 🚢 Deployment

\`\`\`bash
# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Staging  
docker compose -f docker-compose.yml -f docker-compose.staging.yml up -d
\`\`\`

## 📞 Supporto

Per supporto tecnico: [support@stakc.dev](mailto:support@stakc.dev)  
Documentazione: [docs.stakc.dev](https://docs.stakc.dev)

---
*Generato automaticamente da STAKC GDPR Template*
EOF

# Final setup
echo -e "${BLUE}🔧 Setup finale...${NC}"

# Make scripts executable
find scripts/ -name "*.sh" -type f -exec chmod +x {} \;

# Create necessary directories
mkdir -p logs exports backups temp

# Set permissions
chmod 600 .env
chmod -R 755 scripts/

echo ""
echo -e "${GREEN}🎉 PROGETTO CREATO CON SUCCESSO! 🎉${NC}"
echo ""
echo -e "${BLUE}📁 Directory: ${GREEN}$PROJECT_DIR${NC}"
echo -e "${BLUE}🚀 Per avviare:${NC}"
echo -e "   ${YELLOW}cd $PROJECT_NAME${NC}"
echo -e "   ${YELLOW}docker compose up -d${NC}"
echo ""
echo -e "${BLUE}🌐 URL di accesso:${NC}"
echo -e "   ${GREEN}• Applicazione: http://$DOMAIN${NC}"
echo -e "   ${GREEN}• API Docs: http://$DOMAIN/docs${NC}"
echo -e "   ${GREEN}• Admin: http://$DOMAIN/admin${NC}"
if [ "$ENVIRONMENT" = "development" ]; then
    echo -e "   ${GREEN}• MailHog: http://$DOMAIN:8025${NC}"
fi
echo ""
echo -e "${BLUE}🛡️ GDPR Compliance: ${GREEN}ATTIVA${NC}"
echo -e "${BLUE}🔒 Security: ${GREEN}ATTIVA${NC}"
echo ""
echo -e "${YELLOW}⚠️  Ricorda di:${NC}"
echo -e "   • Modificare le password in .env per production"
echo -e "   • Configurare SMTP per invio email"  
echo -e "   • Verificare i domini in Caddyfile per HTTPS"
echo ""
echo -e "${GREEN}✨ Buon sviluppo con STAKC GDPR Template! ✨${NC}"