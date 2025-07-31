# STAKC GDPR Template 🚀

Un template modulare, scalabile e GDPR-compliant per qualsiasi progetto (Blog, E-commerce, Document Management, CRM, SaaS, ecc).


## Caratteristiche Principali

- Architettura a plugin: GDPR, Security, Analytics, Audit, Notification
- Business logic separata dai plugin
- Frontend e backend pronti all’uso
- Setup istantaneo per nuovi progetti
- Compliance GDPR automatica
- Configurazione centralizzata via `.env`
- Test automatici e API documentate
- Supporto Docker, Kubernetes, Caddy, Celery
- Template frontend: Next.js, React, Vue, HTML
- Documentazione completa (`docs/`)


---

## Come Iniziare

### 1. Clona il repository

```bash
git clone <repo-url>
cd stack-gdpr-template
```

### 2. Configura le variabili d’ambiente

Copia `.env.example` in `.env` e personalizza:

```bash
cp .env.example .env
```

### 3. Avvia i servizi con Docker Compose

```bash
docker compose up --build
```

### 4. Crea un nuovo progetto (opzionale)

```bash
./scripts/setup/new-project.sh --name="my-blog" --template="blog" --plugins="gdpr,security,analytics"
```

---

## Plugin System 🔌

- **GDPR**: Consensi, export, cancellazione, audit
- **Security**: Rate limiting, bot detection, IP blocking
- **Analytics**: Metriche business
- **Audit**: Logging avanzato
- **Notification**: Email, Slack, SMS

Abilita/disabilita plugin modificando `ENABLED_PLUGINS` in `.env`:

```env
ENABLED_PLUGINS=gdpr,security,analytics,audit,notification
```

Ogni plugin è completamente isolato e riutilizzabile. Puoi aggiungere nuovi plugin creando una cartella in `plugins/` e seguendo la struttura base.

---

## Esempi di Progetto

- Blog aziendale
- E-commerce
- Gestione documenti
- CRM
- SaaS Platform

Trovi esempi concreti nella cartella `examples/`.

---

## Frontend

Trovi template React/Next.js, Vanilla HTML, Vue, ecc. nella cartella `frontend_templates/`.
Ogni template include componenti modulari per privacy, consensi e export dati.

Esempio Next.js:
- `components/plugins/gdpr/CookieConsentBanner.tsx`
- `components/plugins/gdpr/PrivacyDashboard.tsx`
- `components/plugins/gdpr/DataExportButton.tsx`

---

## API & Test

- Tutte le API sono documentate via OpenAPI (Swagger: `/docs`)
- Test automatici con `pytest` (vedi cartelle `tests/` e `plugins/*/test_api.py`)
- Esempi di chiamata API in `plugins/analytics_plugin/api_examples.http`

---

## Best Practice

- Business logic separata dai plugin
- Compliance GDPR automatica
- Configurazione centralizzata via `.env`
- Plugin Manager per carico dinamico
- Frontend modulare con componenti privacy
- Audit trail e logging avanzato
- Sicurezza by design (rate limiting, bot protection, security headers)
- Supporto multi-tenant e multi-template

---

## Deployment

- Docker Compose pronto all’uso (`docker-compose.yml`)
- Supporto Kubernetes (`config/deployment/kubernetes/`)
- Reverse proxy Caddy (`Caddyfile.template`)
- Celery per task e scheduler
- Backup automatici e audit log

---

## Documentazione

Consulta la cartella `docs/` per guide dettagliate su:

- Architettura
- Sviluppo plugin
- Compliance GDPR
- Sicurezza
- Deployment
- API core e plugin
- Template frontend

---

## FAQ & Supporto

- **Come aggiungo un nuovo plugin?**
  - Crea una cartella in `plugins/`, implementa `plugin.py`, `api.py`, `models.py`, `services.py`.
  - Aggiungi il nome del plugin a `ENABLED_PLUGINS` in `.env`.
- **Come cambio template frontend?**
  - Modifica `FRONTEND_TEMPLATE` in `.env`.
- **Come esporto i dati GDPR?**
  - Usa l’endpoint `/gdpr/export` o il componente frontend `DataExportButton`.
- **Come personalizzo la business logic?**
  - Modifica i file in `project_templates/<nome_template>/`.

---

## Supporto

Per domande, personalizzazioni o bug, consulta la documentazione (`docs/`) o apri una issue su GitHub.

---

*Powered by STAKC GDPR Template v2.0.0*
