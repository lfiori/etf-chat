"""
e2e/conftest.py — Fixtures per i test Playwright (avvio server reale).
"""
import subprocess
import time
import os
import pytest
import requests


SERVER_URL = "http://localhost:8765"


@pytest.fixture(scope="session")
def live_server():
    """Avvia il server FastAPI in un processo separato e attende che sia pronto."""
    env = os.environ.copy()
    env.setdefault("ANTHROPIC_API_KEY", "test-key-placeholder")

    proc = subprocess.Popen(
        ["uvicorn", "app:app", "--port", "8765", "--log-level", "error"],
        env=env,
        cwd=os.path.join(os.path.dirname(__file__), "../.."),
    )

    # Attende fino a 15s che il server risponda
    for _ in range(30):
        try:
            requests.get(f"{SERVER_URL}/api/stats", timeout=1)
            break
        except Exception:
            time.sleep(0.5)
    else:
        proc.terminate()
        pytest.fail("Il server non si è avviato in tempo")

    yield SERVER_URL

    proc.terminate()
    proc.wait()


@pytest.fixture(scope="session")
def browser_page(live_server):
    """Pagina Playwright collegata al server live."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()
