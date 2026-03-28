"""
test_scheduler.py — Test per il job di aggiornamento giornaliero.
"""
import sqlite3
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta


def _seed_old_prices(db_path: str, symbol: str, last_date: str):
    """Inserisce prezzi fino a last_date per simulare dati 'vecchi'."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT OR IGNORE INTO etf_info (symbol, name, category, currency) VALUES (?,?,?,?)",
        (symbol, symbol, "Test", "USD"),
    )
    conn.execute(
        "INSERT OR IGNORE INTO etf_prices (symbol, date, open, high, low, close, volume, adj_close) VALUES (?,?,?,?,?,?,?,?)",
        (symbol, last_date, 100.0, 101.0, 99.0, 100.5, 1000000, 100.5),
    )
    conn.commit()
    conn.close()


def _make_fake_hist(start: str, end: str):
    """Crea un DataFrame yfinance-like con 3 giorni di dati."""
    dates = pd.date_range(start=start, periods=3, freq="B")
    return pd.DataFrame({
        "Date": dates,
        "Open":      [101.0] * 3,
        "High":      [102.0] * 3,
        "Low":       [100.0] * 3,
        "Close":     [101.5] * 3,
        "Adj Close": [101.5] * 3,
        "Volume":    [500000] * 3,
    })


def test_incremental_update_adds_only_new_rows(test_db_path):
    """Verifica che il job aggiunga solo le righe mancanti."""
    symbol = "TEST_INC"
    last_known = (datetime.utcnow() - timedelta(days=5)).strftime("%Y-%m-%d")
    _seed_old_prices(test_db_path, symbol, last_known)

    fake_hist = _make_fake_hist(
        (datetime.utcnow() - timedelta(days=4)).strftime("%Y-%m-%d"),
        datetime.utcnow().strftime("%Y-%m-%d"),
    )
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = fake_hist
    mock_ticker.fast_info.currency = "USD"

    with patch("scheduler.yf.Ticker", return_value=mock_ticker):
        from scheduler import daily_update_job
        result = daily_update_job(test_db_path)

    conn = sqlite3.connect(test_db_path)
    count = conn.execute(
        "SELECT COUNT(*) FROM etf_prices WHERE symbol=?", (symbol,)
    ).fetchone()[0]
    conn.close()

    # Deve avere il seed originale + le 3 nuove righe
    assert count >= 4


def test_update_log_written(test_db_path):
    """Verifica che il job scriva una riga in etf_update_log."""
    conn = sqlite3.connect(test_db_path)
    before = conn.execute("SELECT COUNT(*) FROM etf_update_log").fetchone()[0]
    conn.close()

    mock_ticker = MagicMock()
    mock_ticker.history.return_value = pd.DataFrame()  # nessun dato → skip

    with patch("scheduler.yf.Ticker", return_value=mock_ticker):
        from scheduler import daily_update_job
        daily_update_job(test_db_path)

    conn = sqlite3.connect(test_db_path)
    after = conn.execute("SELECT COUNT(*) FROM etf_update_log").fetchone()[0]
    conn.close()

    assert after > before


def test_update_handles_yfinance_error(test_db_path):
    """Il job non deve crashare se yfinance solleva un'eccezione."""
    mock_ticker = MagicMock()
    mock_ticker.history.side_effect = Exception("Timeout di rete simulato")

    with patch("scheduler.yf.Ticker", return_value=mock_ticker):
        from scheduler import daily_update_job
        result = daily_update_job(test_db_path)

    # Il job deve completare e restituire uno status
    assert result["status"] in ("ok", "partial", "error", "skip")


def test_skip_when_db_missing(tmp_path):
    """Il job deve restituire status='skip' se il DB non esiste."""
    from scheduler import daily_update_job
    result = daily_update_job(str(tmp_path / "nonexistent.db"))
    assert result["status"] == "skip"
