"""
test_frontend.py — Test end-to-end con Playwright.
Richiedono un server in esecuzione.
Eseguire con: pytest -m e2e
"""
import pytest

BASE = "http://localhost:8765"


@pytest.mark.e2e
def test_chat_page_loads(browser_page):
    browser_page.goto(BASE)
    assert "ETF Chat" in browser_page.title()
    assert browser_page.locator("#sidebar").is_visible()
    assert browser_page.locator("#user-input").is_visible()


@pytest.mark.e2e
def test_sidebar_has_nav_links(browser_page):
    browser_page.goto(BASE)
    assert browser_page.locator("a[href='/admin.html']").is_visible()
    assert browser_page.locator("a[href='/etf-manager.html']").is_visible()


@pytest.mark.e2e
def test_db_status_shows(browser_page):
    browser_page.goto(BASE)
    browser_page.wait_for_selector("#db-status", timeout=5000)
    status_text = browser_page.locator("#db-status").inner_text()
    assert len(status_text) > 0


@pytest.mark.e2e
def test_new_chat_button_clears(browser_page):
    browser_page.goto(BASE)
    # Clicca "nuova chat" e verifica che il welcome sia visibile
    browser_page.click("#btn-new-chat")
    browser_page.wait_for_selector("#welcome", timeout=3000)


@pytest.mark.e2e
def test_admin_page_loads(browser_page):
    browser_page.goto(f"{BASE}/admin.html")
    assert "Admin" in browser_page.title()
    browser_page.wait_for_selector("#summary-cards", timeout=5000)
    assert browser_page.locator("#summary-cards").is_visible()


@pytest.mark.e2e
def test_etf_manager_page_loads(browser_page):
    browser_page.goto(f"{BASE}/etf-manager.html")
    assert "ETF Manager" in browser_page.title()
    browser_page.wait_for_selector("#etf-table", timeout=5000)
    assert browser_page.locator("#etf-table").is_visible()


@pytest.mark.e2e
def test_etf_manager_shows_catalog(browser_page):
    browser_page.goto(f"{BASE}/etf-manager.html")
    # Attende che le righe della tabella siano caricate
    browser_page.wait_for_selector("#tbody tr", timeout=8000)
    rows = browser_page.locator("#tbody tr").count()
    assert rows > 50   # il catalogo ha 200+ ETF
