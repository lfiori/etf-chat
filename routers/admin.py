"""
routers/admin.py — Endpoints per la dashboard admin:
  GET  /api/admin/stats
  GET  /api/admin/sessions
  GET  /api/admin/timeline
  GET  /api/admin/last-update
  POST /api/admin/trigger-update
"""
import os
import sqlite3
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/admin", tags=["admin"])

# DB_PATH viene importato da app.py tramite dipendenza
def _get_db_path() -> str:
    return os.environ.get("ETF_DB_PATH", "etf_database.db")


def _conn(db_path: str):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


@router.get("/stats")
def admin_stats(
    start: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end:   Optional[str] = Query(None, description="YYYY-MM-DD"),
):
    db = _get_db_path()
    if not os.path.exists(db):
        raise HTTPException(503, "Database non trovato")

    where, params = _date_where(start, end)
    conn = _conn(db)
    c = conn.cursor()

    total_sessions = c.execute(
        f"SELECT COUNT(DISTINCT session_id) FROM access_log {where}", params
    ).fetchone()[0]

    total_messages = c.execute(
        f"SELECT COUNT(*) FROM access_log WHERE event_type='user_message' {_and(where)}", params
    ).fetchone()[0]

    total_responses = c.execute(
        f"SELECT COUNT(*) FROM access_log WHERE event_type='ai_response' {_and(where)}", params
    ).fetchone()[0]

    tokens = c.execute(
        f"SELECT COALESCE(SUM(input_tokens),0), COALESCE(SUM(output_tokens),0) "
        f"FROM access_log WHERE event_type='ai_response' {_and(where)}", params
    ).fetchone()

    date_range = c.execute(
        "SELECT MIN(date), MAX(date) FROM access_log"
    ).fetchone()

    conn.close()
    return {
        "total_sessions":  total_sessions,
        "total_messages":  total_messages,
        "total_responses": total_responses,
        "total_input_tokens":  tokens[0],
        "total_output_tokens": tokens[1],
        "data_from": date_range[0],
        "data_to":   date_range[1],
    }


@router.get("/sessions")
def admin_sessions(
    start: Optional[str] = Query(None),
    end:   Optional[str] = Query(None),
    page:  int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
):
    db = _get_db_path()
    if not os.path.exists(db):
        raise HTTPException(503, "Database non trovato")

    where, params = _date_where(start, end)
    conn = _conn(db)
    c = conn.cursor()

    # Sessioni paginate (ordinate per prima attività)
    offset = (page - 1) * limit
    sessions_rows = c.execute(
        f"""SELECT DISTINCT session_id, MIN(timestamp) AS first_at, MAX(timestamp) AS last_at,
               COUNT(CASE WHEN event_type='user_message' THEN 1 END) AS msg_count
            FROM access_log {where}
            GROUP BY session_id
            ORDER BY first_at DESC
            LIMIT ? OFFSET ?""",
        (*params, limit, offset),
    ).fetchall()

    total_sessions = c.execute(
        f"SELECT COUNT(DISTINCT session_id) FROM access_log {where}", params
    ).fetchone()[0]

    sessions = []
    for s in sessions_rows:
        sid = s["session_id"]
        exchanges = c.execute(
            """SELECT event_type, timestamp, message_text, response_text,
                      input_tokens, output_tokens, elapsed_ms, iterations, sql_count
               FROM access_log
               WHERE session_id = ? AND event_type IN ('user_message','ai_response')
               ORDER BY timestamp""",
            (sid,),
        ).fetchall()
        sessions.append({
            "session_id": sid,
            "first_at":   s["first_at"],
            "last_at":    s["last_at"],
            "msg_count":  s["msg_count"],
            "exchanges":  [dict(e) for e in exchanges],
        })

    conn.close()
    return {
        "sessions": sessions,
        "total":    total_sessions,
        "page":     page,
        "limit":    limit,
    }


@router.get("/timeline")
def admin_timeline(
    start: Optional[str] = Query(None),
    end:   Optional[str] = Query(None),
):
    db = _get_db_path()
    if not os.path.exists(db):
        raise HTTPException(503, "Database non trovato")

    where, params = _date_where(start, end)
    conn = _conn(db)
    rows = conn.execute(
        f"""SELECT date,
               COUNT(DISTINCT session_id)                                         AS sessions,
               COUNT(CASE WHEN event_type='user_message'  THEN 1 END)            AS messages,
               COALESCE(SUM(CASE WHEN event_type='ai_response' THEN input_tokens  ELSE 0 END),0) AS input_tokens,
               COALESCE(SUM(CASE WHEN event_type='ai_response' THEN output_tokens ELSE 0 END),0) AS output_tokens
            FROM access_log {where}
            GROUP BY date
            ORDER BY date""",
        params,
    ).fetchall()
    conn.close()
    return {"timeline": [dict(r) for r in rows]}


@router.get("/last-update")
def last_update():
    db = _get_db_path()
    if not os.path.exists(db):
        return {"last_update": None}
    try:
        conn = _conn(db)
        row = conn.execute(
            "SELECT run_at, etfs_updated, rows_added, status FROM etf_update_log ORDER BY id DESC LIMIT 1"
        ).fetchone()
        conn.close()
        return {"last_update": dict(row) if row else None}
    except Exception:
        return {"last_update": None}


@router.post("/trigger-update")
async def trigger_update():
    """Avvia manualmente l'aggiornamento giornaliero degli ETF."""
    try:
        from scheduler import daily_update_job
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, daily_update_job)
        return {"ok": True, "message": "Aggiornamento avviato in background"}
    except Exception as e:
        raise HTTPException(500, str(e))


# ── helpers ──────────────────────────────────────────────────────────────────

def _date_where(start: Optional[str], end: Optional[str]):
    clauses, params = [], []
    if start:
        clauses.append("date >= ?")
        params.append(start)
    if end:
        clauses.append("date <= ?")
        params.append(end)
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    return where, tuple(params)


def _and(where: str) -> str:
    """Aggiunge AND se c'è già una clausola WHERE, altrimenti aggiunge WHERE."""
    return "AND" if where else "WHERE"
