"""
test_sql_helper.py — Unit test per execute_sql e _StdDev.
"""
import pytest


def test_select_allowed(test_db_path):
    from app import execute_sql
    result = execute_sql("SELECT symbol FROM etf_info ORDER BY symbol")
    assert "error" not in result
    assert result["row_count"] == 3
    assert result["columns"] == ["symbol"]


def test_with_cte_allowed(test_db_path):
    from app import execute_sql
    result = execute_sql("WITH t AS (SELECT symbol FROM etf_info) SELECT * FROM t")
    assert "error" not in result


def test_insert_blocked(test_db_path):
    from app import execute_sql
    result = execute_sql("INSERT INTO etf_info VALUES ('X','X','X','USD','2024-01-01')")
    assert "error" in result
    assert "SELECT" in result["error"]


def test_drop_blocked(test_db_path):
    from app import execute_sql
    result = execute_sql("DROP TABLE etf_info")
    assert "error" in result


def test_delete_blocked(test_db_path):
    from app import execute_sql
    result = execute_sql("DELETE FROM etf_info")
    assert "error" in result


def test_missing_db_returns_error(monkeypatch):
    import app as app_module
    monkeypatch.setattr(app_module, "DB_PATH", "/nonexistent/db.sqlite")
    result = app_module.execute_sql("SELECT 1")
    assert "error" in result


def test_stdev_aggregate(test_db_path):
    from app import execute_sql
    result = execute_sql(
        "WITH dr AS (SELECT symbol, adj_close / LAG(adj_close) OVER (PARTITION BY symbol ORDER BY date) - 1 AS r "
        "FROM etf_prices WHERE symbol='SPY') "
        "SELECT STDEV(r) AS vol FROM dr WHERE r IS NOT NULL"
    )
    assert "error" not in result
    assert result["data"][0]["vol"] is not None
    assert result["data"][0]["vol"] > 0


def test_empty_result(test_db_path):
    from app import execute_sql
    result = execute_sql("SELECT * FROM etf_info WHERE symbol='NONEXISTENT'")
    assert "error" not in result
    assert result["row_count"] == 0
