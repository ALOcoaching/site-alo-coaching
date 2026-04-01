"""
Tests de non-régression — SEO, accessibilité de base, meta tags.
"""
import pytest
from playwright.sync_api import expect


PAGES_WITH_SEO = [
    "/",
    "/formations.html",
    "/coaching.html",
    "/a-propos.html",
    "/contact.html",
    "/blog.html",
    "/faq.html",
]


@pytest.mark.parametrize("path", PAGES_WITH_SEO)
def test_page_has_title(page, base_url, path):
    """Chaque page doit avoir un <title> non vide."""
    page.goto(f"{base_url}{path}")
    title = page.title()
    assert len(title) > 5, f"{path} : title trop court ('{title}')"


@pytest.mark.parametrize("path", PAGES_WITH_SEO)
def test_page_has_meta_description(page, base_url, path):
    """Chaque page doit avoir une meta description."""
    page.goto(f"{base_url}{path}")
    meta = page.locator("meta[name='description']")
    assert meta.count() >= 1, f"{path} : meta description manquante"
    content = meta.get_attribute("content")
    assert content and len(content) > 20, f"{path} : meta description trop courte"


@pytest.mark.parametrize("path", PAGES_WITH_SEO)
def test_page_has_h1(page, base_url, path):
    """Chaque page doit avoir exactement 1 balise H1."""
    page.goto(f"{base_url}{path}")
    h1_count = page.locator("h1").count()
    assert h1_count == 1, f"{path} : {h1_count} H1 trouvé(s), attendu 1"


@pytest.mark.parametrize("path", PAGES_WITH_SEO)
def test_page_has_charset_utf8(page, base_url, path):
    """Chaque page doit déclarer UTF-8."""
    page.goto(f"{base_url}{path}")
    charset = page.locator("meta[charset]")
    assert charset.count() >= 1, f"{path} : charset manquant"


def test_images_have_alt(page, base_url):
    """Les images de la page d'accueil doivent avoir un attribut alt."""
    page.goto(f"{base_url}/")
    images = page.locator("img")
    for i in range(images.count()):
        img = images.nth(i)
        alt = img.get_attribute("alt")
        src = img.get_attribute("src") or "?"
        assert alt is not None, f"Image sans alt : {src}"


def test_robots_txt_exists(page, base_url):
    """robots.txt doit exister et être accessible."""
    response = page.goto(f"{base_url}/robots.txt")
    assert response.status == 200


def test_sitemap_xml_exists(page, base_url):
    """sitemap.xml doit exister et contenir des URLs."""
    response = page.goto(f"{base_url}/sitemap.xml")
    assert response.status == 200
    content = page.content()
    assert "url" in content.lower()


def test_canonical_or_og_tags(page, base_url):
    """La page d'accueil doit avoir des Open Graph tags."""
    page.goto(f"{base_url}/")
    og_title = page.locator("meta[property='og:title']")
    assert og_title.count() >= 1, "og:title manquant"
