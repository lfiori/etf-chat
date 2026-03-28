"""
scheduler.py — Aggiornamento giornaliero incrementale dei prezzi ETF.
Avvio automatico tramite APScheduler (BackgroundScheduler) in-process.
"""
import logging
import os
import sqlite3
import time
from datetime import datetime, timedelta

import yfinance as yf
import pandas as pd

log = logging.getLogger("etf-chat")

DB_PATH = os.environ.get("ETF_DB_PATH", "etf_database.db")


def daily_update_job(db_path: str = None) -> dict:
    """
    Per ogni ETF in etf_info:
      1. Trova la data massima già presente in etf_prices
      2. Scarica i dati dal giorno successivo a oggi
      3. Inserisce solo le righe nuove (INSERT OR IGNORE)
    Registra il risultato in etf_update_log.
    """
    from db_tracking import record_update_log

    db = db_path or DB_PATH
    if not os.path.exists(db):
        log.warning("scheduler: database non trovato, skip", extra={"event": "scheduler_skip"})
        return {"status": "skip", "reason": "db_not_found"}

    t0 = time.monotonic()
    today = datetime.utcnow().strftime("%Y-%m-%d")

    conn = sqlite3.connect(db, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")

    symbols = [r[0] for r in conn.execute("SELECT symbol FROM etf_info").fetchall()]
    log.info("scheduler_start", extra={
        "event": "scheduler_start", "etf_count": len(symbols), "date": today
    })

    updated, failed, total_rows = 0, 0, 0

    for symbol in symbols:
        try:
            row = conn.execute(
                "SELECT MAX(date) FROM etf_prices WHERE symbol = ?", (symbol,)
            ).fetchone()
            last_date = row[0] if row and row[0] else None

            if last_date and last_date >= today:
                continue  # già aggiornato oggi

            start = (
                (datetime.strptime(last_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
                if last_date else
                (datetime.utcnow() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")
            )

            ticker = yf.Ticker(symbol)
            hist = ticker.history(start=start, end=today, auto_adjust=False)

            if hist.empty:
                continue

            hist = hist.reset_index()
            hist["Date"] = pd.to_datetime(hist["Date"]).dt.strftime("%Y-%m-%d")
            adj_col = "Adj Close" if "Adj Close" in hist.columns else "Close"

            rows = []
            for _, r in hist.iterrows():
                vol = r.get("Volume", 0)
                rows.append((
                    symbol,
                    r["Date"],
                    float(r["Open"])   if pd.notna(r.get("Open"))   else None,
                    float(r["High"])   if pd.notna(r.get("High"))   else None,
                    float(r["Low"])    if pd.notna(r.get("Low"))    else None,
                    float(r["Close"])  if pd.notna(r.get("Close"))  else None,
                    int(vol)           if pd.notna(vol)             else 0,
                    float(r[adj_col]) if pd.notna(r.get(adj_col))  else None,
                ))

            conn.executemany(
                """INSERT OR IGNORE INTO etf_prices
                   (symbol, date, open, high, low, close, volume, adj_close)
                   VALUES (?,?,?,?,?,?,?,?)""",
                rows,
            )
            conn.execute(
                "UPDATE etf_info SET last_updated=? WHERE symbol=?", (today, symbol)
            )
            conn.commit()
            total_rows += len(rows)
            updated += 1
            time.sleep(0.3)

        except Exception as exc:
            failed += 1
            log.warning("scheduler_etf_error", extra={
                "event": "scheduler_etf_error", "symbol": symbol, "error": str(exc)
            })

    conn.close()
    duration = round(time.monotonic() - t0, 2)
    status = "ok" if failed == 0 else ("partial" if updated > 0 else "error")

    log.info("scheduler_done", extra={
        "event": "scheduler_done",
        "updated": updated, "failed": failed,
        "rows_added": total_rows, "duration_sec": duration, "status": status,
    })

    record_update_log(
        db_path=db,
        etfs_updated=updated,
        etfs_failed=failed,
        rows_added=total_rows,
        duration_sec=duration,
        status=status,
        notes=f"{failed} ETF falliti" if failed else None,
    )

    return {
        "status": status, "updated": updated,
        "failed": failed, "rows_added": total_rows,
        "duration_sec": duration,
    }


def create_scheduler(db_path: str = None):
    """Crea e configura il BackgroundScheduler. Chiamato da app.py."""
    from apscheduler.schedulers.background import BackgroundScheduler

    sched = BackgroundScheduler(daemon=True)
    sched.add_job(
        lambda: daily_update_job(db_path),
        trigger="cron",
        hour=6, minute=0,
        id="daily_etf_update",
        replace_existing=True,
        misfire_grace_time=3600,
    )
    return sched
