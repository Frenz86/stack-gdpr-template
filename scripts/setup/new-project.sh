#!/bin/bash
# Crea nuovo progetto GDPR-compliant
set -e

# Default values
PROJECT_NAME=""
TEMPLATE=""
PLUGINS=""
FRONTEND=""

# Parse named arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --name=*)
      PROJECT_NAME="${1#*=}"
      shift
      ;;
    --template=*)
      TEMPLATE="${1#*=}"
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
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [ -z "$PROJECT_NAME" ] || [ -z "$TEMPLATE" ] || [ -z "$PLUGINS" ]; then
  echo "Usage: $0 --name=NAME --template=TEMPLATE --plugins=PLUGINS [--frontend=FRONTEND]"
  exit 1
fi

# Setup base
TEMPLATE_DIR="project_templates/$TEMPLATE"
if [ ! -d "$TEMPLATE_DIR" ]; then
  echo "Template directory '$TEMPLATE_DIR' does not exist."
  exit 1
fi
cp -r "$TEMPLATE_DIR" "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Crea file .env con ENABLED_PLUGINS in formato JSON
cat <<EOF > .env
ENABLED_PLUGINS='["$(echo $PLUGINS | sed 's/,/","/g')"]'
EOF

# Attiva plugin
for plugin in $(echo $PLUGINS | tr "," "\n"); do
  echo "Attivazione plugin: $plugin"
  # Placeholder per attivazione plugin
done

# Setup frontend
if [ "$FRONTEND" != "" ]; then
  echo "Setup frontend: $FRONTEND"
  # Placeholder per setup frontend
fi

# Setup frontend (build automatico se Next.js)
if [ -d "../frontend_templates/nextjs_base" ]; then
  echo "Costruzione frontend Next.js..."
  cd ../frontend_templates/nextjs_base
  if [ -f "package.json" ]; then
    npm install && npm run build
    # Sposta la cartella out in dist per compatibilità con Caddy/docker-compose
    if [ -d "out" ]; then
      rm -rf dist && mv out dist
    else
      echo "⚠️  Build Next.js fallita: controlla che tutte le pagine abbiano un export default valido."
    fi
  fi
  cd - > /dev/null
fi

echo "✅ Progetto '$PROJECT_NAME' creato e configurato"
