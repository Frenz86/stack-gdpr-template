# Guida Blog GDPR: Avvio, Monitoring e Deploy

Questa guida ti accompagna passo passo per creare, monitorare e distribuire un blog GDPR-ready con lo stack STAKC, anche senza competenze tecniche.

---

## 1. Prerequisiti

- Docker Desktop installato
- (Opzionale) Node.js per modifiche frontend
- Connessione Internet

---

## 2. Clona il repository

Scarica il progetto dal repository GitHub:

```bash
git clone <repo-url> demo-blog
cd demo-blog
```

---

## 3. Setup progetto

1. Esegui:

    ```bash
    bash setup-project.sh --name=demo-blog --template=blog --plugins=gdpr,security,analytics --frontend=nextjs_base --domain=localhost
    ```

2. Avvia i servizi:

    ```bash
    docker compose up -d
    ```

---

## 4. Accesso e Monitoring

- Blog: [http://localhost](http://localhost)
- API Docs: [http://localhost/docs](http://localhost/docs)
- Admin Panel: [http://localhost/admin](http://localhost/admin)
- Dashboard GDPR: [http://localhost/admin/gdpr](http://localhost/admin/gdpr)

> Nota: La dashboard GDPR ([http://localhost/admin/gdpr](http://localhost/admin/gdpr)) è accessibile senza login nella configurazione demo. In produzione, l'accesso sarà protetto da autenticazione admin.

### Monitoring Dashboard (real-time)

Esempio componenti (TypeScript/React):

```typescript
<ComplianceDashboard>
  <GDPRMetrics />
  <SecurityThreats />
  <PluginHealth />
</ComplianceDashboard>
```

- **GDPRMetrics**: consensi, richieste export/cancellazione, privacy policy
- **SecurityThreats**: tentativi di attacco, IP bloccati
- **PluginHealth**: stato e performance plugin

---

## 5. Multi-Cloud Deployment

Puoi distribuire il blog su vari ambienti:

```yaml
deployment_targets:
  - docker_compose
  - kubernetes
  - aws_ecs
  - google_cloud_run
```

- **docker_compose**: locale/server
- **kubernetes**: cluster scalabile
- **aws_ecs**: Amazon ECS
- **google_cloud_run**: Google Cloud Run

Consulta `config/deployment/` per esempi e guide.

---

## 6. Personalizzazione e sviluppo

- Modifica contenuti in `project_templates/blog/`
- Personalizza frontend in `frontend_templates/nextjs_base/`
- Attiva/disattiva plugin in `.env`

---

## 7. Troubleshooting

- Se qualcosa non funziona, riavvia Docker Desktop e ripeti i comandi
- Consulta la documentazione in `docs/`
- Per aiuto, apri una issue su GitHub

---

Blog pronto, dashboard GDPR attiva, deploy multi-cloud supportato!
