#!/usr/bin/env python3
"""
ETF Chat — Backend FastAPI con Claude API (text-to-SQL via tool use).

Avvio: uvicorn app:app --reload --port 8000
"""

import json
import logging
import os
import sqlite3
import time

from dotenv import load_dotenv
load_dotenv()
import uuid
from typing import Optional

from pythonjsonlogger import jsonlogger

_handler = logging.StreamHandler()
_formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    rename_fields={"asctime": "time", "levelname": "level", "name": "logger"},
)
_handler.setFormatter(_formatter)
log = logging.getLogger("etf-chat")
log.setLevel(logging.INFO)
log.addHandler(_handler)
log.propagate = False

import anthropic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ─────────────────────────── configurazione ────────────────────────────────
DB_PATH = "etf_database.db"
MAX_ROWS = 500        # righe massime restituite da una query
MAX_ITERATIONS = 12   # iterazioni massime del loop agente

app = FastAPI(title="ETF Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic()   # legge ANTHROPIC_API_KEY dall'ambiente

# Sessioni in-memory (dizionario session_id → lista messaggi)
sessions: dict[str, list] = {}

# ─────────────────────────── system prompt ─────────────────────────────────
SYSTEM_PROMPT = """Sei un esperto analista finanziario con accesso diretto a un database SQLite
di ETF (Exchange-Traded Fund). Rispondi sempre nella stessa lingua dell'utente.

═══════════════════════ SCHEMA DEL DATABASE ═══════════════════════

Tabella `etf_info`  — metadati ETF
  symbol       TEXT  PK   — ticker (es. 'SPY', 'QQQ', 'GLD')
  name         TEXT       — nome completo
  category     TEXT       — categoria/settore
  currency     TEXT       — valuta di negoziazione (solitamente 'USD')
  last_updated TEXT       — data ultimo aggiornamento YYYY-MM-DD

Tabella `etf_prices`  — prezzi storici giornalieri (~5 anni)
  symbol    TEXT  PK  — ticker ETF
  date      TEXT  PK  — data YYYY-MM-DD
  open      REAL       — prezzo apertura
  high      REAL       — massimo giornaliero
  low       REAL       — minimo giornaliero
  close     REAL       — prezzo chiusura
  volume    INTEGER    — volume scambiato
  adj_close REAL       — prezzo adjusted (corretto per dividendi e split)

Indici disponibili: (symbol), (date), (symbol, date)

═══════════════════════ REGOLE IMPORTANTI ════════════════════════

1. Usa SEMPRE `adj_close` per calcoli di rendimento/performance.
2. Rendimento % = (adj_close_finale - adj_close_iniziale) / adj_close_iniziale * 100
3. Per la volatilità annualizzata usa la deviazione standard delle variazioni
   giornaliere (%) moltiplicata per SQRT(252).
4. Le date sono TEXT in formato YYYY-MM-DD — usa operatori stringa per confronti.
5. Esegui più query se necessario per rispondere in modo completo.
6. Quando i risultati sono molto numerosi, riassumi i punti chiave.
7. Presenta i numeri in modo leggibile (es. "12,4%" non "12.4321...").

═══════════════════════ QUERY DI ESEMPIO ════════════════════════

-- Migliori performer nell'ultimo anno:
WITH range AS (
  SELECT symbol,
         FIRST_VALUE(adj_close) OVER (PARTITION BY symbol ORDER BY date) AS first_p,
         LAST_VALUE(adj_close)  OVER (PARTITION BY symbol ORDER BY date
                                      ROWS BETWEEN UNBOUNDED PRECEDING
                                               AND UNBOUNDED FOLLOWING) AS last_p
  FROM etf_prices
  WHERE date >= DATE('now', '-1 year')
)
SELECT i.symbol, i.name, i.category,
       ROUND((MAX(last_p) - MAX(first_p)) / MAX(first_p) * 100, 2) AS return_pct
FROM range r JOIN etf_info i USING(symbol)
GROUP BY r.symbol ORDER BY return_pct DESC LIMIT 10;

-- Volatilità annualizzata:
WITH daily_ret AS (
  SELECT symbol, (adj_close / LAG(adj_close) OVER (PARTITION BY symbol ORDER BY date) - 1) AS r
  FROM etf_prices
  WHERE date >= DATE('now', '-1 year')
)
SELECT symbol, ROUND(STDEV(r) * SQRT(252) * 100, 2) AS vol_pct
FROM daily_ret WHERE r IS NOT NULL
GROUP BY symbol ORDER BY vol_pct DESC;
"""

# ─────────────────────────── tool definition ───────────────────────────────
TOOLS = [
    {
        "name": "execute_sql",
        "description": (
            "Esegui una query SQL SELECT sul database ETF SQLite. "
            "Usa questa funzione per recuperare prezzi storici, calcolare "
            "performance, confrontare ETF, analizzare volumi e trend."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Query SQL SELECT valida per SQLite",
                }
            },
            "required": ["query"],
        },
    }
]

# ─────────────────────────── helpers ───────────────────────────────────────

def execute_sql(query: str) -> dict:
    """Esegue la query e restituisce un dict serializzabile."""
    q = query.strip()
    upper = q.upper()
    # Whitelist: solo SELECT e WITH (CTE)
    if not (upper.startswith("SELECT") or upper.startswith("WITH")):
        return {"error": "Sono ammesse solo query SELECT/WITH per motivi di sicurezza."}

    if not os.path.exists(DB_PATH):
        return {"error": f"Database '{DB_PATH}' non trovato. Esegui prima setup_database.py."}

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        # STDEV user-defined aggregate (non presente di default in SQLite)
        conn.create_aggregate("STDEV", 1, _StdDev)
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchall()
        conn.close()

        if not rows:
            return {"columns": [], "data": [], "row_count": 0}

        columns = list(rows[0].keys())
        data = [dict(r) for r in rows[:MAX_ROWS]]
        return {
            "columns": columns,
            "data": data,
            "row_count": len(data),
            "total_rows": len(rows),
            "truncated": len(rows) > MAX_ROWS,
        }
    except Exception as exc:
        return {"error": f"Errore SQL: {exc}"}


class _StdDev:
    """Aggregato SQLite per STDEV (deviazione standard campionaria)."""

    def __init__(self):
        self.values = []

    def step(self, value):
        if value is not None:
            self.values.append(float(value))

    def finalize(self):
        n = len(self.values)
        if n < 2:
            return None
        mean = sum(self.values) / n
        variance = sum((x - mean) ** 2 for x in self.values) / (n - 1)
        return variance ** 0.5


def _content_to_dicts(content) -> list:
    """Converte i blocchi Anthropic in dizionari serializzabili."""
    result = []
    for block in content:
        if not hasattr(block, "type"):
            continue
        if block.type == "text":
            result.append({"type": "text", "text": block.text})
        elif block.type == "tool_use":
            result.append(
                {
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input,
                }
            )
    return result


# ─────────────────────────── modelli request/response ──────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


# ─────────────────────────── endpoints ─────────────────────────────────────

@app.post("/api/chat")
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())

    if session_id not in sessions:
        sessions[session_id] = []

    messages = sessions[session_id]
    messages.append({"role": "user", "content": req.message})

    sql_queries: list[str] = []
    _t_start = time.monotonic()
    total_input_tokens = 0
    total_output_tokens = 0
    iteration_details: list[dict] = []

    log.info("user_message", extra={
        "event": "user_message",
        "session": session_id,
        "message_preview": req.message[:120],
    })

    for iteration in range(MAX_ITERATIONS):
        log.info("claude_call", extra={
            "event": "claude_call",
            "session": session_id,
            "iteration": iteration + 1,
        })
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        total_input_tokens  += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens

        log.info("claude_call", extra={
            "event": "claude_call",
            "session": session_id,
            "iteration": iteration + 1,
            "stop_reason": response.stop_reason,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        })

        _iter_sql_calls: list[dict] = []
        content_dicts = _content_to_dicts(response.content)
        messages.append({"role": "assistant", "content": content_dicts})

        if response.stop_reason == "end_turn":
            iteration_details.append({
                "iteration": iteration + 1,
                "stop_reason": "end_turn",
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "sql_calls": [],
            })
            final_text = next(
                (b.text for b in response.content if b.type == "text"),
                "Nessuna risposta generata.",
            )
            elapsed_ms = round((time.monotonic() - _t_start) * 1000)
            log.info("response_ready", extra={
                "event": "response_ready",
                "session": session_id,
                "response_length": len(final_text),
                "iterations": iteration + 1,
                "elapsed_ms": elapsed_ms,
            })
            sessions[session_id] = messages
            return {
                "response": final_text,
                "session_id": session_id,
                "sql_queries": sql_queries,
                "trace": {
                    "iterations": iteration + 1,
                    "elapsed_ms": elapsed_ms,
                    "total_tokens": {
                        "input": total_input_tokens,
                        "output": total_output_tokens,
                        "total": total_input_tokens + total_output_tokens,
                    },
                    "iteration_details": iteration_details,
                },
            }

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type != "tool_use" or block.name != "execute_sql":
                    continue
                query = block.input.get("query", "")
                sql_queries.append(query)
                result = execute_sql(query)
                _sql_call: dict = {"query": query, "row_count": None, "error": None}
                if "error" in result:
                    _sql_call["error"] = result["error"]
                    log.warning("sql_error", extra={
                        "event": "sql_error",
                        "session": session_id,
                        "query": query.replace("\n", " "),
                        "error": result["error"],
                    })
                else:
                    _sql_call["row_count"] = result.get("row_count", 0)
                    log.info("sql_executed", extra={
                        "event": "sql_executed",
                        "session": session_id,
                        "query": query.replace("\n", " "),
                        "row_count": _sql_call["row_count"],
                    })
                _iter_sql_calls.append(_sql_call)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, ensure_ascii=False, default=str),
                })

            iteration_details.append({
                "iteration": iteration + 1,
                "stop_reason": "tool_use",
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "sql_calls": _iter_sql_calls,
            })

            if tool_results:
                messages.append({"role": "user", "content": tool_results})
        else:
            log.warning("max_iterations_exceeded", extra={
                "event": "max_iterations_exceeded",
                "session": session_id,
                "stop_reason": response.stop_reason,
            })
            iteration_details.append({
                "iteration": iteration + 1,
                "stop_reason": response.stop_reason,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "sql_calls": [],
            })
            break

    elapsed_ms = round((time.monotonic() - _t_start) * 1000)
    log.warning("max_iterations_exceeded", extra={
        "event": "max_iterations_exceeded",
        "session": session_id,
        "iterations": MAX_ITERATIONS,
        "elapsed_ms": elapsed_ms,
    })
    sessions[session_id] = messages
    return {
        "response": "Elaborazione terminata senza una risposta definitiva.",
        "session_id": session_id,
        "sql_queries": sql_queries,
        "trace": {
            "iterations": len(iteration_details),
            "elapsed_ms": elapsed_ms,
            "total_tokens": {
                "input": total_input_tokens,
                "output": total_output_tokens,
                "total": total_input_tokens + total_output_tokens,
            },
            "iteration_details": iteration_details,
        },
    }


@app.post("/api/chat/new")
async def new_session():
    """Crea una nuova sessione di chat."""
    sid = str(uuid.uuid4())
    sessions[sid] = []
    return {"session_id": sid}


@app.delete("/api/chat/{session_id}")
async def delete_session(session_id: str):
    """Elimina una sessione."""
    sessions.pop(session_id, None)
    return {"ok": True}


@app.get("/api/stats")
async def stats():
    """Statistiche sul database."""
    if not os.path.exists(DB_PATH):
        raise HTTPException(
            status_code=503,
            detail="Database non trovato. Esegui prima: python setup_database.py",
        )
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    etf_count   = c.execute("SELECT COUNT(*) FROM etf_info").fetchone()[0]
    price_count = c.execute("SELECT COUNT(*) FROM etf_prices").fetchone()[0]
    date_range  = c.execute("SELECT MIN(date), MAX(date) FROM etf_prices").fetchone()
    categories  = c.execute(
        "SELECT category, COUNT(*) FROM etf_info GROUP BY category ORDER BY 2 DESC LIMIT 15"
    ).fetchall()
    conn.close()
    return {
        "etf_count":    etf_count,
        "price_records": price_count,
        "date_from":    date_range[0],
        "date_to":      date_range[1],
        "categories":   [{"name": r[0], "count": r[1]} for r in categories],
    }


@app.get("/api/etfs")
async def list_etfs():
    """Elenco di tutti gli ETF disponibili."""
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=503, detail="Database non trovato.")
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT symbol, name, category, currency FROM etf_info ORDER BY symbol"
    ).fetchall()
    conn.close()
    return {"etfs": [{"symbol": r[0], "name": r[1], "category": r[2], "currency": r[3]} for r in rows]}


# Serve il frontend statico (deve essere l'ultimo mount)
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
