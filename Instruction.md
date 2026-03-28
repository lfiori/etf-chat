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
