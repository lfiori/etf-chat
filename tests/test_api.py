"""
test_api.py — Test degli endpoint FastAPI.
"""
import pytest


def test_stats_endpoint(client):
    res = client.get("/api/stats")
    assert res.status_code == 200
    d = res.json()
    assert "etf_count" in d
    assert "price_records" in d
    assert d["etf_count"] == 3


def test_etfs_endpoint(client):
    res = client.get("/api/etfs")
    assert res.status_code == 200
    d = res.json()
    assert "etfs" in d
    assert len(d["etfs"]) == 3
    first = d["etfs"][0]
    assert "symbol" in first
    assert "name" in first
    assert "category" in first
    assert "currency" in first


def test_new_session(client):
    res = client.post("/api/chat/new")
    assert res.status_code == 200
    assert "session_id" in res.json()


def test_delete_session(client):
    res = client.post("/api/chat/new")
    sid = res.json()["session_id"]
    del_res = client.delete(f"/api/chat/{sid}")
    assert del_res.status_code == 200
    assert del_res.json()["ok"] is True


def test_admin_stats_endpoint(client):
    res = client.get("/api/admin/stats")
    assert res.status_code == 200
    d = res.json()
    assert "total_sessions" in d
    assert "total_messages" in d
    assert "total_input_tokens" in d


def test_admin_timeline_endpoint(client):
    res = client.get("/api/admin/timeline")
    assert res.status_code == 200
    d = res.json()
    assert "timeline" in d
    assert isinstance(d["timeline"], list)


def test_admin_sessions_endpoint(client):
    res = client.get("/api/admin/sessions")
    assert res.status_code == 200
    d = res.json()
    assert "sessions" in d
    assert "total" in d


def test_admin_last_update_endpoint(client):
    res = client.get("/api/admin/last-update")
    assert res.status_code == 200
    assert "last_update" in res.json()


def test_etf_catalog_endpoint(client):
    res = client.get("/api/etf-manager/catalog")
    assert res.status_code == 200
    d = res.json()
    assert "catalog" in d
    assert len(d["catalog"]) > 100   # il catalogo ha 200+ ETF
    first = d["catalog"][0]
    assert "symbol" in first
    assert "group_name" in first
    assert "is_in_db" in first


def test_etf_manager_status_endpoint(client):
    res = client.get("/api/etf-manager/status")
    assert res.status_code == 200
    d = res.json()
    assert "running" in d
    assert d["running"] is False


def test_admin_stats_date_filter(client):
    res = client.get("/api/admin/stats?start=2020-01-01&end=2020-12-31")
    assert res.status_code == 200
    d = res.json()
    assert d["total_sessions"] == 0   # nessun dato in quel periodo nel test DB


def test_admin_timeline_date_filter(client):
    res = client.get("/api/admin/timeline?start=2024-01-01&end=2024-01-31")
    assert res.status_code == 200
