"""
db_tracking.py — Gestione tabelle di tracking: access_log, etf_update_log, etf_catalog.
"""
import sqlite3
from datetime import datetime, date


def get_conn(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


def create_tracking_tables(db_path: str) -> None:
    """Crea le tabelle di tracking se non esistono."""
    conn = get_conn(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS access_log (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type    TEXT NOT NULL,
            session_id    TEXT NOT NULL,
            timestamp     TEXT NOT NULL,
            date          TEXT NOT NULL,
            message_text  TEXT,
            response_text TEXT,
            input_tokens  INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            elapsed_ms    INTEGER DEFAULT 0,
            sql_count     INTEGER DEFAULT 0,
            iterations    INTEGER DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_access_log_date
            ON access_log(date);
        CREATE INDEX IF NOT EXISTS idx_access_log_session
            ON access_log(session_id);
        CREATE INDEX IF NOT EXISTS idx_access_log_event_type
            ON access_log(event_type);

        CREATE TABLE IF NOT EXISTS etf_update_log (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            run_at        TEXT NOT NULL,
            date          TEXT NOT NULL,
            etfs_updated  INTEGER DEFAULT 0,
            etfs_failed   INTEGER DEFAULT 0,
            rows_added    INTEGER DEFAULT 0,
            duration_sec  REAL DEFAULT 0,
            status        TEXT DEFAULT 'ok',
            notes         TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_update_log_date
            ON etf_update_log(date);

        CREATE TABLE IF NOT EXISTS etf_catalog (
            symbol        TEXT PRIMARY KEY,
            name          TEXT NOT NULL,
            category      TEXT NOT NULL,
            group_name    TEXT NOT NULL,
            region        TEXT,
            currency      TEXT DEFAULT 'USD',
            is_in_db      INTEGER DEFAULT 0,
            notes         TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_catalog_group
            ON etf_catalog(group_name);
        CREATE INDEX IF NOT EXISTS idx_catalog_region
            ON etf_catalog(region);
    """)
    conn.commit()
    conn.close()


def record_access(
    db_path: str,
    event_type: str,
    session_id: str,
    message_text: str = None,
    response_text: str = None,
    input_tokens: int = 0,
    output_tokens: int = 0,
    elapsed_ms: int = 0,
    sql_count: int = 0,
    iterations: int = 0,
) -> None:
    now = datetime.utcnow()
    conn = get_conn(db_path)
    conn.execute(
        """INSERT INTO access_log
           (event_type, session_id, timestamp, date,
            message_text, response_text,
            input_tokens, output_tokens, elapsed_ms, sql_count, iterations)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (
            event_type, session_id,
            now.strftime("%Y-%m-%dT%H:%M:%S"),
            now.strftime("%Y-%m-%d"),
            message_text, response_text,
            input_tokens, output_tokens, elapsed_ms, sql_count, iterations,
        ),
    )
    conn.commit()
    conn.close()


def record_update_log(
    db_path: str,
    etfs_updated: int,
    etfs_failed: int,
    rows_added: int,
    duration_sec: float,
    status: str = "ok",
    notes: str = None,
) -> None:
    now = datetime.utcnow()
    conn = get_conn(db_path)
    conn.execute(
        """INSERT INTO etf_update_log
           (run_at, date, etfs_updated, etfs_failed, rows_added, duration_sec, status, notes)
           VALUES (?,?,?,?,?,?,?,?)""",
        (
            now.strftime("%Y-%m-%dT%H:%M:%S"),
            now.strftime("%Y-%m-%d"),
            etfs_updated, etfs_failed, rows_added,
            duration_sec, status, notes,
        ),
    )
    conn.commit()
    conn.close()


def seed_catalog_table_from_setup(db_path: str) -> None:
    """Popola etf_catalog dal catalogo completo (chiamato da setup_database)."""
    from etf_catalog import seed_catalog_table
    seed_catalog_table(db_path)
    sync_catalog_is_in_db(db_path)


def sync_catalog_is_in_db(db_path: str) -> None:
    """Aggiorna il flag is_in_db nella tabella etf_catalog."""
    conn = get_conn(db_path)
    conn.execute("UPDATE etf_catalog SET is_in_db = 0")
    conn.execute("""
        UPDATE etf_catalog SET is_in_db = 1
        WHERE symbol IN (SELECT symbol FROM etf_info)
    """)
    conn.commit()
    conn.close()
