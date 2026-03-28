"""
conftest.py — Fixtures condivise per tutti i test backend.
"""
import os
import sqlite3
import pytest
from fastapi.testclient import TestClient


# ── Database di test ──────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def test_db_path(tmp_path_factory):
    """
    Crea un database SQLite isolato con schema completo e dati minimi.
    Viene creato una sola volta per sessione di test.
    """
    db = str(tmp_path_factory.mktemp("data") / "test_etf.db")
    os.environ["ETF_DB_PATH"] = db

    conn = sqlite3.connect(db)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS etf_info (
            symbol TEXT PRIMARY KEY, name TEXT, category TEXT,
            currency TEXT DEFAULT 'USD', last_updated TEXT
        );
        CREATE TABLE IF NOT EXISTS etf_prices (
            symbol TEXT NOT NULL, date TEXT NOT NULL,
            open REAL, high REAL, low REAL, close REAL,
            volume INTEGER, adj_close REAL,
            PRIMARY KEY (symbol, date)
        );
        CREATE INDEX IF NOT EXISTS idx_prices_symbol ON etf_prices(symbol);
        CREATE INDEX IF NOT EXISTS idx_prices_date   ON etf_prices(date);
    """)

    # Seed: 3 ETF con 20 giorni di prezzi
    etfs = [
        ("SPY", "SPDR S&P 500 ETF Trust", "US Large Cap", "USD", "2024-01-20"),
        ("QQQ", "Invesco QQQ Trust",       "US Technology", "USD", "2024-01-20"),
        ("GLD", "SPDR Gold Shares",         "Gold",          "USD", "2024-01-20"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO etf_info VALUES (?,?,?,?,?)", etfs
    )

    import random, math
    random.seed(42)
    prices = []
    base = {"SPY": 400.0, "QQQ": 350.0, "GLD": 180.0}
    for sym, start_price in base.items():
        p = start_price
        for i in range(20):
            date = f"2024-01-{i+1:02d}"
            p = p * (1 + random.uniform(-0.02, 0.02))
            prices.append((sym, date, round(p*0.99,2), round(p*1.01,2),
                           round(p*0.98,2), round(p,2), 1000000, round(p,2)))
    conn.executemany(
        "INSERT OR IGNORE INTO etf_prices VALUES (?,?,?,?,?,?,?,?)", prices
    )
    conn.commit()
    conn.close()

    # Crea tabelle tracking
    from db_tracking import create_tracking_tables
    create_tracking_tables(db)

    return db


@pytest.fixture(scope="session")
def client(test_db_path):
    """FastAPI TestClient configurato con il database di test."""
    from app import app
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=False)
def clean_access_log(test_db_path):
    """Pulisce access_log prima di ogni test che lo usa."""
    conn = sqlite3.connect(test_db_path)
    conn.execute("DELETE FROM access_log")
    conn.commit()
    conn.close()
    yield
