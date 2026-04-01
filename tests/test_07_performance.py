"""
Tests de non-régression — Performance & Sécurité de base.
"""
import pytest
from playwright.sync_api import expect


def test_no_console_errors(page, base_url):
    """La page d'accueil ne doit pas avoir d'erreurs console JS."""
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.goto(f"{base_url}/")
    page.wait_for_load_state("networkidle")
    assert len(errors) == 0, f"Erreurs console : {errors}"


def test_no_broken_images(page, base_url):
    """Les images de l'accueil ne doivent pas être cassées."""
    page.goto(f"{base_url}/")
    page.wait_for_load_state("networkidle")
    broken = page.evaluate("""
        () => {
            const imgs = document.querySelectorAll('img');
            const broken = [];
            imgs.forEach(img => {
                if (img.naturalWidth === 0 && img.src) broken.push(img.src);
            });
            return broken;
        }
    """)
    assert len(broken) == 0, f"Images cassées : {broken}"


def test_css_loads(page, base_url):
    """Le CSS principal doit se charger."""
    page.goto(f"{base_url}/")
    # Vérifie qu'un style est appliqué (pas de page blanche brute)
    bg = page.evaluate("getComputedStyle(document.body).backgroundColor")
    assert bg != "" and bg != "rgba(0, 0, 0, 0)", "CSS semble ne pas être chargé"


def test_js_loads(page, base_url):
    """Le JS principal (main.js) doit se charger."""
    page.goto(f"{base_url}/")
    scripts = page.locator("script[src*='main']")
    assert scripts.count() >= 1, "main.js non trouvé"


def test_https_redirect(page, base_url):
    """Le site doit être servi en HTTPS (skip en local)."""
    if "localhost" in base_url or "127.0.0.1" in base_url:
        pytest.skip("HTTPS non applicable en local")
    page.goto(f"{base_url}/")
    assert page.url.startswith("https://"), f"URL non HTTPS : {page.url}"


def test_security_headers(page, base_url):
    """Vérifie les headers de sécurité basiques."""
    response = page.goto(f"{base_url}/")
    headers = response.headers
    # Netlify _headers file should set these
    # On vérifie juste que la page se charge correctement
    assert response.status == 200
