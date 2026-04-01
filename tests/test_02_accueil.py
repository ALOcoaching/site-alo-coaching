"""
Tests de non-régression — Page d'accueil (index.html).
Vérifie le hero, les stats, les sections clés, le CTA.
"""
from playwright.sync_api import expect


def test_hero_title(page, base_url):
    """Le titre hero principal doit être visible."""
    page.goto(f"{base_url}/")
    h1 = page.locator("h1")
    expect(h1).to_be_visible()
    assert "chef" in h1.inner_text().lower() or "projet" in h1.inner_text().lower()


def test_hero_cta_buttons(page, base_url):
    """Les boutons CTA du hero doivent exister."""
    page.goto(f"{base_url}/")
    cta = page.locator(".hero .btn, .hero-content .btn")
    assert cta.count() >= 1, "Au moins 1 bouton CTA dans le hero"


def test_stats_section(page, base_url):
    """La section stats (30 ans, etc.) doit être visible."""
    page.goto(f"{base_url}/")
    stats = page.locator(".hero-stat, .stat, [data-count]")
    assert stats.count() >= 1, "Au moins 1 stat sur la page d'accueil"


def test_formations_section(page, base_url):
    """La section formations phares doit exister."""
    page.goto(f"{base_url}/")
    assert "formation" in page.content().lower()


def test_temoignages_section(page, base_url):
    """La section témoignages doit exister."""
    page.goto(f"{base_url}/")
    assert "client" in page.content().lower() or "moignage" in page.content().lower()


def test_no_english_on_homepage(page, base_url):
    """Pas de texte en anglais visible sur l'accueil (hors code/attributs)."""
    page.goto(f"{base_url}/")
    body_text = page.locator("body").inner_text().lower()
    english_markers = ["thank you", "submit", "click here", "read more", "learn more"]
    for marker in english_markers:
        assert marker not in body_text, f"Texte anglais détecté : '{marker}'"
