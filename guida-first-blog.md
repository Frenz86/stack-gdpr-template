# Guida Pratica: Crea il tuo primo Blog GDPR-compliant con STAKC

Questa guida ti accompagna passo passo, anche se non hai competenze tecniche, per creare un blog moderno e sicuro, conforme al GDPR, usando lo stack STAKC. Segui le istruzioni e avrai subito accesso alla dashboard di controllo GDPR.

---

## 1. Prerequisiti minimi

- Un computer con Windows, Mac o Linux
- Connessione a Internet
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installato (gratuito)
- [Node.js](https://nodejs.org/) installato (solo se vuoi modificare il frontend)

Non serve conoscere Python, Linux o programmazione!

---

## 2. Scarica il progetto

1. Vai su [GitHub](https://github.com/Frenz86/stack-gdpr-template) e scarica il progetto come ZIP
2. Estrai la cartella sul desktop (es: `C:\Users\tuonome\Desktop\demo-blog`)

---

## 3. Avvia il blog

1. Apri Docker Desktop e assicurati che sia attivo
2. Apri una finestra "Prompt dei comandi" (Windows) o "Terminale" (Mac/Linux)
3. Vai nella cartella del progetto:

   ```bash
   cd Desktop/demo-blog
   ```

4. Avvia il blog con un solo comando:

   ```bash
   bash setup-project.sh --name=demo-blog --template=blog --plugins=gdpr,security,analytics --frontend=nextjs_base --domain=localhost
   ```

   > Lo script prepara tutto in automatico: database, backend, frontend, sicurezza, privacy.

5. Avvia i servizi:

   ```bash
   docker compose up -d
   ```

---

## 4. Accedi al tuo blog

- Apri il browser e vai su [http://localhost](http://localhost)
- Il tuo blog è già online!

---

## 5. Accedi alla dashboard GDPR

- Vai su [http://localhost/admin/gdpr](http://localhost/admin/gdpr)
- Qui puoi:
  - Vedere i consensi raccolti
  - Gestire richieste di export/cancellazione dati
  - Monitorare le notifiche di sicurezza
  - Visualizzare l’audit trail e le versioni della privacy policy

---

## 6. Personalizza il blog (facoltativo)

- Modifica i contenuti nella cartella `project_templates/blog/`
- Cambia il logo, i colori o i testi nel frontend (`frontend_templates/nextjs_base/`)
- Tutto è modulare e sicuro: puoi aggiungere plugin, metriche, notifiche

---

## 7. Risoluzione problemi

- Se qualcosa non funziona, riavvia Docker Desktop e ripeti i comandi
- Consulta la documentazione nella cartella `docs/`
- Per aiuto, apri una issue su GitHub o chiedi al tuo referente tecnico

---

Complimenti! Hai creato il tuo primo blog GDPR-ready, con dashboard di controllo privacy e sicurezza.

Buon blogging!
