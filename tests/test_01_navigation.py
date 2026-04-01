"""
Tests de non-régression — Navigation & structure du site.
Vérifie que toutes les pages existent, se chargent, et que la navigation fonctionne.
"""
import pytest
from playwright.sync_api import expect

# ══════════════════════════════════════════════════════════════
# Toutes les pages du site
# ══════════════════════════════════════════════════════════════
PAGES = [
    ("/index.html", "ALO Coaching"),
    ("/formations.html", "Formations"),
    ("/coaching.html", "Coaching"),
    ("/a-propos.html", "propos"),
    ("/contact.html", "Contact"),
    ("/blog.html", "Blog"),
    ("/blog-article-1.html", "erreurs"),
    ("/blog-article-2.html", "offshore"),
    ("/blog-article-3.html", "portfolio"),
    ("/blog-article-4.html", "interculturel"),
    ("/faq.html", "FAQ"),
    ("/temoignages.html", "moignages"),
    ("/forfait-it.html", "Forfait"),
    ("/lead-magnet.html", "PDF"),
    ("/mentions-legales.html", "Mentions"),
    ("/politique-confidentialite.html", "Confidentialit"),
    ("/merci.html", "envoy"),
]


@pytest.mark.parametrize("path, expected_text", PAGES)
def test_page_loads_200(page, base_url, path, expected_text):
    """Chaque page doit retourner HTTP 200 et contenir du texte attendu."""
    response = page.goto(f"{base_url}{path}")
    assert response.status == 200, f"{path} retourne {response.status}"
    assert expected_text.lower() in page.content().lower(), \
        f"'{expected_text}' non trouvé dans {path}"


def test_html_lang_fr(page, base_url):
    """Toutes les pages doivent avoir lang='fr'."""
    for path, _ in PAGES:
        page.goto(f"{base_url}{path}")
        html_tag = page.locator("html")
        expect(html_tag).to_have_attribute("lang", "fr")


# ══════════════════════════════════════════════════════════════
# Navigation principale
# ══════════════════════════════════════════════════════════════
def test_navbar_present(page, base_url):
    """La navbar doit être présente sur la page d'accueil."""
    page.goto(f"{base_url}/")
    navbar = page.locator("nav.navbar")
    expect(navbar).to_be_visible()


def test_navbar_links(page, base_url):
    """Les liens principaux de navigation doivent exister."""
    page.goto(f"{base_url}/")
    expected_links = ["Accueil", "Formations", "Coaching", "propos", "Contact"]
    for text in expected_links:
        link = page.locator(f"nav a:has-text('{text}')")
        expect(link.first).to_be_visible()


def test_navbar_navigation(page, base_url):
    """Cliquer sur un lien de navigation doit mener à la bonne page."""
    page.goto(f"{base_url}/")
    page.locator("nav a:has-text('Formations')").first.click()
    page.wait_for_load_state("networkidle")
    assert "formation" in page.url.lower()


def test_logo_links_to_home(page, base_url):
    """Le logo doit ramener à l'accueil."""
    page.goto(f"{base_url}/formations.html")
    page.locator("a.nav-logo").click()
    page.wait_for_load_state("networkidle")
    assert page.url.rstrip("/") == base_url.rstrip("/") or "index" in page.url.lower()


# ══════════════════════════════════════════════════════════════
# Footer
# ══════════════════════════════════════════════════════════════
def test_footer_present(page, base_url):
    """Le footer doit être présent avec le copyright."""
    page.goto(f"{base_url}/")
    footer = page.locator("footer")
    expect(footer).to_be_visible()
    assert "2026" in footer.inner_text()
    assert "ALO" in footer.inner_text()
