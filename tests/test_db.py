"""
test_db.py — Test per le funzioni di db_tracking.
"""
import sqlite3
import pytest
from db_tracking import (
    create_tracking_tables, record_access, record_update_log,
    sync_catalog_is_in_db,
)


def test_tracking_tables_created(test_db_path):
    conn = sqlite3.connect(test_db_path)
    tables = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()}
    conn.close()
    assert "access_log"    in tables
    assert "etf_update_log" in tables
    assert "etf_catalog"   in tables


def test_record_access_insert(test_db_path, clean_access_log):
    record_access(
        test_db_path, "user_message", "sess-001",
        message_text="Ciao!", input_tokens=10, output_tokens=5,
    )
    conn = sqlite3.connect(test_db_path)
    row = conn.execute(
        "SELECT * FROM access_log WHERE session_id='sess-001'"
    ).fetchone()
    conn.close()
    assert row is not None
    assert row[1] == "user_message"   # event_type
    assert row[6] == "Ciao!"          # message_text


def test_record_access_ai_response(test_db_path, clean_access_log):
    record_access(
        test_db_path, "ai_response", "sess-002",
        response_text="La risposta è X",
        input_tokens=100, output_tokens=50,
        elapsed_ms=1200, sql_count=2, iterations=3,
    )
    conn = sqlite3.connect(test_db_path)
    row = conn.execute(
        "SELECT input_tokens, output_tokens, elapsed_ms, sql_count, iterations "
        "FROM access_log WHERE session_id='sess-002'"
    ).fetchone()
    conn.close()
    assert row == (100, 50, 1200, 2, 3)


def test_record_update_log(test_db_path):
    record_update_log(
        test_db_path, etfs_updated=50, etfs_failed=2,
        rows_added=5000, duration_sec=45.3, status="partial",
        notes="2 ETF falliti",
    )
    conn = sqlite3.connect(test_db_path)
    row = conn.execute(
        "SELECT etfs_updated, rows_added, status FROM etf_update_log ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.close()
    assert row[0] == 50
    assert row[1] == 5000
    assert row[2] == "partial"


def test_date_index_exists(test_db_path):
    conn = sqlite3.connect(test_db_path)
    indexes = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='index'"
    ).fetchall()}
    conn.close()
    assert "idx_access_log_date" in indexes


def test_sync_catalog_is_in_db(test_db_path):
    from etf_catalog import seed_catalog_table
    seed_catalog_table(test_db_path)
    sync_catalog_is_in_db(test_db_path)

    conn = sqlite3.connect(test_db_path)
    spy_row = conn.execute(
        "SELECT is_in_db FROM etf_catalog WHERE symbol='SPY'"
    ).fetchone()
    unk_row = conn.execute(
        "SELECT is_in_db FROM etf_catalog WHERE symbol='QQQ'"
    ).fetchone()
    conn.close()
    # SPY e QQQ sono nel test DB (seed), quindi is_in_db=1
    assert spy_row[0] == 1
    assert unk_row[0] == 1
