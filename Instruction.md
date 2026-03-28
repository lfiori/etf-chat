# Deploy su GitHub e Render

## Prerequisiti

- [GitHub CLI](https://cli.github.com) installato
- Account [render.com](https://render.com) creato
- Database `etf_database.db` generato (`python setup_database.py`)

---

## 1. Crea il repo GitHub e fai il primo push

Apri il terminale nella cartella del progetto ed esegui:

```bash
cd c:\Users\emara\etf-chat
git init
git add .gitignore render.yaml requirements.txt app.py setup_database.py static/ etf_database.db
git commit -m "Initial commit"
gh auth login
gh repo create etf-chat --public --source=. --remote=origin --push
```

> Il file `.env` (con la tua API key) **non** viene incluso grazie al `.gitignore`.

---

## 2. Deploy su Render

1. Vai su [render.com](https://render.com) → **New → Web Service**
2. Connetti il tuo account GitHub e seleziona il repo `etf-chat`
3. Render rileva automaticamente il file `render.yaml`
4. Nella sezione **Environment Variables**, aggiungi:
   - Key: `ANTHROPIC_API_KEY`
   - Value: la tua chiave Anthropic
5. Nel campo **Start Command** inserisci:
   ```
   uvicorn app:app --host 0.0.0.0 --port $PORT
   ```
6. Clicca **Deploy**

Dopo ~2 minuti l'app sarà raggiungibile su un URL tipo:
```
https://etf-chat.onrender.com
```

---

## Note

- Il piano gratuito di Render mette il servizio in **sleep dopo 15 minuti** di inattività. Il primo accesso dopo una pausa richiede ~30 secondi per il riavvio.
- Render inietta automaticamente la variabile `$PORT`, non è necessario modificare nulla nell'app.
- Per aggiornare l'app dopo modifiche al codice, basta fare un nuovo `git push` — Render si aggiorna automaticamente.

---

## 3. Usare Git per salvare gli avanzamenti

Git salva "fotografie" del tuo codice chiamate **commit**.

### Prima volta (già fatto per questo progetto)
```bash
git init                  # inizializza il repo
git remote add origin URL # collega a GitHub
```

### Flusso quotidiano

```bash
# 1. Vedi cosa è cambiato
git status

# 2. Aggiungi i file che vuoi salvare
git add app.py            # file specifico
git add .                 # tutti i file modificati

# 3. Crea il commit (la "fotografia")
git commit -m "descrizione di cosa hai fatto"

# 4. Carica su GitHub
git push
```

### Comandi utili

```bash
git log --oneline         # cronologia dei commit
git diff                  # mostra le modifiche non ancora aggiunte
git restore app.py        # annulla le modifiche a un file (ATTENZIONE: irreversibile)
```

### Regola pratica

> Fai un commit ogni volta che completi qualcosa di funzionante — una feature, una correzione, una modifica significativa. Il messaggio deve spiegare **cosa** hai fatto, es: `"aggiunto pannello trace nella UI"`.

---

## 4. Pipeline di test

### Cos'è e a cosa serve

La pipeline di test verifica automaticamente che l'app funzioni correttamente. È composta da 4 livelli:

| Tipo | File | Cosa verifica | Velocità |
|---|---|---|---|
| **Unitari** | `test_sql_helper.py`, `test_db.py` | Singole funzioni (SQL, database) | ~1s |
| **Integrazione** | `test_api.py` | Tutti gli endpoint HTTP | ~2s |
| **Scheduler** | `test_scheduler.py` | Aggiornamento giornaliero ETF (con dati finti) | ~2s |
| **Qualità chat** | `test_quality.py` | Correttezza delle risposte AI (Claude-as-judge) | ~30s |
| **Browser (E2E)** | `e2e/test_frontend.py` | Interfaccia grafica nel browser reale | ~20s |

### Installazione (prima volta)

```bash
pip install -r requirements.txt
playwright install chromium   # solo se vuoi eseguire i test browser
```

### Come eseguire i test

```bash
# Test veloci (default) — non richiedono API key né server avviato
pytest

# Test di qualità — richiedono ANTHROPIC_API_KEY e database popolato
pytest -m quality

# Test browser (E2E) — avviano automaticamente un server su porta 8765
pytest -m e2e

# Tutti i test insieme
pytest -m ""

# Un singolo file con output dettagliato
pytest tests/test_api.py -v
```

### Come funziona ogni livello

**Test unitari** — testano funzioni singole in isolamento. Usano un database temporaneo creato appositamente (non toccano mai `etf_database.db`).

**Test di integrazione** — simulano richieste HTTP reali all'app senza avviare un server. Verificano che tutti gli endpoint rispondano con i dati corretti.

**Test scheduler** — sostituiscono yfinance con dati finti (`mock`) per non fare richieste reali a Yahoo Finance. Verificano che il job incrementale funzioni correttamente.

**Test di qualità** — mandano domande reali all'app e usano Claude Haiku come "giudice" per valutare se la risposta è corretta:
```
Domanda → /api/chat → risposta → Claude Haiku → "YES / NO"
```
Richiedono `ANTHROPIC_API_KEY` e consumano token API. Usarli prima di un rilascio importante.

**Test browser (E2E)** — aprono un vero browser Chromium, navigano sull'app e verificano che gli elementi grafici siano visibili e funzionanti (tabella ETF, pagina Admin, link di navigazione, ecc.).

### Struttura dei file di test

```
tests/
├── conftest.py          ← database di test isolato e client HTTP condivisi
├── test_sql_helper.py   ← test esecuzione SQL e sicurezza whitelist
├── test_db.py           ← test tabelle tracking (access_log, ecc.)
├── test_api.py          ← test endpoint /api/*
├── test_scheduler.py    ← test aggiornamento giornaliero ETF
├── test_quality.py      ← test qualità risposte AI (marcati @quality)
└── e2e/
    ├── conftest.py      ← avvio automatico del server per i test browser
    └── test_frontend.py ← test interfaccia Playwright (marcati @e2e)
```

### Nota

I test di qualità e browser sono **esclusi dal default** per non richiedere API key o tempo extra ad ogni esecuzione. Il comando `pytest` senza opzioni esegue solo i test veloci (unitari + integrazione + scheduler).
