"""
routers/etf_manager.py — Gestione ETF nel database:
  GET  /api/etf-manager/catalog
  POST /api/etf-manager/populate
  GET  /api/etf-manager/status
  DELETE /api/etf-manager/remove/{symbol}
"""
import os
import sqlite3
import threading
import time
from datetime import datetime, timedelta
from typing import List

import yfinance as yf
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/etf-manager", tags=["etf-manager"])

# Stato del job di popolamento (in-memory)
_job: dict = {"running": False, "progress": 0, "total": 0, "current": "", "log": [], "last_result": None}
_job_lock = threading.Lock()


def _get_db_path() -> str:
    return os.environ.get("ETF_DB_PATH", "etf_database.db")


def _conn(db_path: str):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.get("/catalog")
def get_catalog():
    """Restituisce il catalogo completo con flag is_in_db."""
    from etf_catalog import FULL_ETF_CATALOG
    db = _get_db_path()

    in_db = set()
    if os.path.exists(db):
        conn = _conn(db)
        rows = conn.execute("SELECT symbol FROM etf_info").fetchall()
        conn.close()
        in_db = {r["symbol"] for r in rows}

    catalog = []
    for e in FULL_ETF_CATALOG:
        catalog.append({
            "symbol":     e["symbol"],
            "name":       e["name"],
            "category":   e["category"],
            "group_name": e["group_name"],
            "region":     e.get("region", ""),
            "currency":   e.get("currency", "USD"),
            "is_in_db":   e["symbol"] in in_db,
        })
    return {"catalog": catalog}


class PopulateRequest(BaseModel):
    symbols: List[str]
    years: int = 5


@router.post("/populate")
def populate(req: PopulateRequest):
    """Avvia il download dei dati per i simboli selezionati (background thread)."""
    with _job_lock:
        if _job["running"]:
            raise HTTPException(409, "Un popolamento è già in corso")
        _job.update(running=True, progress=0, total=len(req.symbols),
                    current="", log=[], last_result=None)

    from etf_catalog import FULL_ETF_CATALOG
    catalog_map = {e["symbol"]: e for e in FULL_ETF_CATALOG}

    def _run():
        db = _get_db_path()
        from setup_database import create_database
        create_database(db)

        conn = sqlite3.connect(db, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")

        start_date = (datetime.utcnow() - timedelta(days=req.years * 365)).strftime("%Y-%m-%d")
        end_date = datetime.utcnow().strftime("%Y-%m-%d")
        ok, fail = 0, 0

        for i, symbol in enumerate(req.symbols, 1):
            meta = catalog_map.get(symbol, {})
            name = meta.get("name", symbol)
            category = meta.get("category", "")

            with _job_lock:
                _job["current"] = symbol
                _job["progress"] = i

            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date, auto_adjust=False)
                if hist.empty:
                    raise ValueError("Nessun dato")

                info = ticker.fast_info
                currency = getattr(info, "currency", "USD") or "USD"

                hist = hist.reset_index()
                hist["Date"] = pd.to_datetime(hist["Date"]).dt.strftime("%Y-%m-%d")
                adj_col = "Adj Close" if "Adj Close" in hist.columns else "Close"

                conn.execute(
                    "INSERT OR REPLACE INTO etf_info (symbol, name, category, currency, last_updated) VALUES (?,?,?,?,?)",
                    (symbol, name, category, currency, end_date),
                )
                rows = []
                for _, r in hist.iterrows():
                    vol = r.get("Volume", 0)
                    rows.append((
                        symbol, r["Date"],
                        float(r["Open"])  if pd.notna(r.get("Open"))  else None,
                        float(r["High"])  if pd.notna(r.get("High"))  else None,
                        float(r["Low"])   if pd.notna(r.get("Low"))   else None,
                        float(r["Close"]) if pd.notna(r.get("Close")) else None,
                        int(vol)          if pd.notna(vol)            else 0,
                        float(r[adj_col]) if pd.notna(r.get(adj_col)) else None,
                    ))
                conn.executemany(
                    "INSERT OR REPLACE INTO etf_prices (symbol, date, open, high, low, close, volume, adj_close) VALUES (?,?,?,?,?,?,?,?)",
                    rows,
                )
                conn.commit()
                ok += 1
                with _job_lock:
                    _job["log"].append(f"✓ {symbol}: {len(rows)} record")
            except Exception as e:
                fail += 1
                with _job_lock:
                    _job["log"].append(f"✗ {symbol}: {e}")

            time.sleep(0.4)

        conn.close()
        from db_tracking import sync_catalog_is_in_db
        sync_catalog_is_in_db(db)

        with _job_lock:
            _job["running"] = False
            _job["last_result"] = {"ok": ok, "fail": fail}

    threading.Thread(target=_run, daemon=True).start()
    return {"ok": True, "message": f"Avviato download di {len(req.symbols)} ETF"}


@router.get("/status")
def populate_status():
    with _job_lock:
        return {
            "running":     _job["running"],
            "progress":    _job["progress"],
            "total":       _job["total"],
            "current":     _job["current"],
            "log":         _job["log"][-50:],   # ultimi 50 messaggi
            "last_result": _job["last_result"],
        }


@router.delete("/remove/{symbol}")
def remove_etf(symbol: str):
    db = _get_db_path()
    if not os.path.exists(db):
        raise HTTPException(503, "Database non trovato")
    conn = _conn(db)
    conn.execute("DELETE FROM etf_prices WHERE symbol = ?", (symbol.upper(),))
    conn.execute("DELETE FROM etf_info WHERE symbol = ?", (symbol.upper(),))
    conn.execute("UPDATE etf_catalog SET is_in_db=0 WHERE symbol=?", (symbol.upper(),))
    conn.commit()
    conn.close()
    return {"ok": True, "symbol": symbol.upper()}
