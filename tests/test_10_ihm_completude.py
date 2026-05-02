"""
Tests de non-régression — Complétude IHM.
Vérifie que tous les éléments visuels critiques sont présents et fonctionnels
sur TOUTES les pages : navbar, footer, CTA, liens, breadcrumbs, témoignages.
"""
import pytest
from playwright.sync_api import expect


# ══════════════════════════════════════════════════════════════
# Données de référence
# ══════════════════════════════════════════════════════════════

# Liens attendus dans la navbar (texte partiel → href attendu)
NAVBAR_LINKS = [
    ("Accueil", "index.html"),
    ("Formations", "formations.html"),
    ("Coaching", "coaching.html"),
    ("moignages", "temoignages.html"),
    ("propos", "a-propos.html"),
    ("FAQ", "faq.html"),
    ("Blog", "blog.html"),
    ("Contact", "contact.html"),
]

# Pages principales avec navbar complète (8 liens + LinkedIn)
PAGES_WITH_FULL_NAVBAR = [
    "/index.html",
    "/formations.html",
    "/coaching.html",
    "/temoignages.html",
    "/a-propos.html",
    "/faq.html",
    "/blog.html",
    "/contact.html",
]

# Liens footer minimum attendus sur toutes les pages
FOOTER_LINKS_MIN = [
    ("Accueil", "index.html"),
    ("Formations", "formations.html"),
    ("Coaching", "coaching.html"),
    ("Contact", "contact.html"),
]

# Pages avec un CTA principal vers contact.html
PAGES_WITH_CONTACT_CTA = [
    "/index.html",
    "/formations.html",
    "/coaching.html",
    "/temoignages.html",
    "/a-propos.html",
    "/faq.html",
    "/forfait-it.html",
]

# Pages avec breadcrumb (Accueil / NomPage)
PAGES_WITH_BREADCRUMB = [
    ("/formations.html", "Formations"),
    ("/coaching.html", "Coaching"),
    ("/temoignages.html", "moignages"),
    ("/a-propos.html", "propos"),
    ("/faq.html", "FAQ"),
    ("/blog.html", "Blog"),
    ("/contact.html", "Contact"),
]


# ══════════════════════════════════════════════════════════════
# 1. NAVBAR — présence et liens corrects sur chaque page
# ══════════════════════════════════════════════════════════════

@pytest.mark.parametrize("page_path", PAGES_WITH_FULL_NAVBAR)
def test_navbar_has_all_links_on_every_page(page, base_url, page_path):
    """Chaque page principale doit avoir les 8 liens de navigation."""
    page.goto(f"{base_url}{page_path}")
    for text, _ in NAVBAR_LINKS:
        link = page.locator(f"nav a:has-text('{text}')")
        assert link.count() >= 1, \
            f"Lien '{text}' absent de la navbar sur {page_path}"


@pytest.mark.parametrize("page_path", PAGES_WITH_FULL_NAVBAR)
def test_navbar_links_point_to_correct_href(page, base_url, page_path):
    """Les liens de la navbar doivent pointer vers les bons fichiers."""
    page.goto(f"{base_url}{page_path}")
    for text, expected_href in NAVBAR_LINKS:
        link = page.locator(f".nav-links a:has-text('{text}')").first
        href = link.get_attribute("href") or ""
        base_name = expected_href.replace(".html", "")
        if base_name == "index":
            assert "index" in href or href in ("/", "./"), \
                f"Sur {page_path}, lien '{text}' pointe vers '{href}' au lieu de '{expected_href}'"
        else:
            assert base_name in href, \
                f"Sur {page_path}, lien '{text}' pointe vers '{href}' au lieu de '{expected_href}'"


@pytest.mark.parametrize("page_path", PAGES_WITH_FULL_NAVBAR)
def test_navbar_linkedin_present(page, base_url, page_path):
    """Le lien LinkedIn doit être dans la navbar de chaque page."""
    page.goto(f"{base_url}{page_path}")
    linkedin = page.locator("nav a[href*='linkedin.com']")
    assert linkedin.count() >= 1, \
        f"Lien LinkedIn absent de la navbar sur {page_path}"


# ══════════════════════════════════════════════════════════════
# 2. FOOTER — présence et liens corrects
# ══════════════════════════════════════════════════════════════

@pytest.mark.parametrize("page_path", PAGES_WITH_FULL_NAVBAR)
def test_footer_has_navigation_links(page, base_url, page_path):
    """Le footer doit contenir les liens de navigation principaux."""
    page.goto(f"{base_url}{page_path}")
    for text, expected_href in FOOTER_LINKS_MIN:
        link = page.locator(f"footer a:has-text('{text}')")
        assert link.count() >= 1, \
            f"Lien footer '{text}' absent sur {page_path}"
        href = link.first.get_attribute("href") or ""
        base_name = expected_href.replace(".html", "")
        if base_name == "index":
            assert "index" in href or href in ("/", "./"), \
                f"Sur {page_path}, footer '{text}' pointe vers '{href}' au lieu de '{expected_href}'"
        else:
            assert base_name in href, \
                f"Sur {page_path}, footer '{text}' pointe vers '{href}' au lieu de '{expected_href}'"


@pytest.mark.parametrize("page_path", PAGES_WITH_FULL_NAVBAR)
def test_footer_has_contact_info(page, base_url, page_path):
    """Le footer doit contenir le téléphone et/ou l'email."""
    page.goto(f"{base_url}{page_path}")
    footer_text = page.locator("footer").inner_text()
    assert "06 80 92 32 59" in footer_text or "arnaud.loyet" in footer_text \
        or "ALO" in footer_text, \
        f"Coordonnées ou marque absentes du footer sur {page_path}"


# ══════════════════════════════════════════════════════════════
# 3. CTA — boutons principaux vers contact
# ══════════════════════════════════════════════════════════════

@pytest.mark.parametrize("page_path", PAGES_WITH_CONTACT_CTA)
def test_cta_contact_present_and_correct(page, base_url, page_path):
    """Chaque page doit avoir au moins un CTA pointant vers contact.html."""
    page.goto(f"{base_url}{page_path}")
    cta = page.locator("a.btn[href*='contact']")
    assert cta.count() >= 1, \
        f"Aucun CTA vers contact.html sur {page_path}"
    href = cta.first.get_attribute("href")
    assert "contact" in href, \
        f"CTA sur {page_path} pointe vers '{href}' au lieu de contact.html"


def test_homepage_hero_cta_formations(page, base_url):
    """Le hero de l'accueil doit avoir un CTA vers formations.html."""
    page.goto(f"{base_url}/index.html")
    cta = page.locator(".hero a.btn[href*='formations']")
    assert cta.count() >= 1, "CTA formations manquant dans le hero"
    href = cta.first.get_attribute("href")
    assert "formations" in href


def test_homepage_hero_cta_contact(page, base_url):
    """Le hero de l'accueil doit avoir un CTA vers contact.html."""
    page.goto(f"{base_url}/index.html")
    cta = page.locator(".hero a.btn[href*='contact']")
    assert cta.count() >= 1, "CTA contact manquant dans le hero"


def test_formations_cta_devis(page, base_url):
    """Les formations doivent avoir des boutons 'Demander un devis' vers contact."""
    page.goto(f"{base_url}/formations.html")
    devis = page.locator("a.btn:has-text('devis')")
    assert devis.count() >= 3, \
        f"Seulement {devis.count()} boutons devis, attendu ≥ 3"
    for i in range(min(devis.count(), 3)):
        href = devis.nth(i).get_attribute("href")
        assert "contact" in href, \
            f"Bouton devis #{i+1} pointe vers '{href}' au lieu de contact.html"


def test_blog_articles_links(page, base_url):
    """Chaque article du blog doit avoir un lien 'Lire l'article'."""
    page.goto(f"{base_url}/blog.html")
    articles = page.locator("a.read-more, .blog-card a[href*='blog-article']")
    assert articles.count() >= 4, \
        f"Seulement {articles.count()} liens d'articles, attendu ≥ 4"


# ══════════════════════════════════════════════════════════════
# 4. BREADCRUMBS
# ══════════════════════════════════════════════════════════════

@pytest.mark.parametrize("page_path, page_name", PAGES_WITH_BREADCRUMB)
def test_breadcrumb_present(page, base_url, page_path, page_name):
    """Les pages intérieures doivent avoir un fil d'Ariane."""
    page.goto(f"{base_url}{page_path}")
    breadcrumb = page.locator(".breadcrumb")
    assert breadcrumb.count() >= 1, \
        f"Breadcrumb absent sur {page_path}"
    bc_text = breadcrumb.inner_text()
    assert "Accueil" in bc_text, \
        f"'Accueil' absent du breadcrumb sur {page_path}"


@pytest.mark.parametrize("page_path, page_name", PAGES_WITH_BREADCRUMB)
def test_breadcrumb_accueil_links_to_index(page, base_url, page_path, page_name):
    """Le lien 'Accueil' du breadcrumb doit pointer vers index.html."""
    page.goto(f"{base_url}{page_path}")
    bc_link = page.locator(".breadcrumb a:has-text('Accueil')")
    assert bc_link.count() >= 1, \
        f"Lien Accueil absent du breadcrumb sur {page_path}"
    href = bc_link.first.get_attribute("href") or ""
    assert "index" in href or href in ("/", "./"), \
        f"Breadcrumb Accueil pointe vers '{href}' sur {page_path}"


# ══════════════════════════════════════════════════════════════
# 5. TÉMOIGNAGES — contenu spécifique
# ══════════════════════════════════════════════════════════════

def test_temoignages_page_abdou_present(page, base_url):
    """Le témoignage d'Abdou S. doit être sur la page témoignages."""
    page.goto(f"{base_url}/temoignages.html")
    text = page.locator("main").inner_text().lower()
    assert "abdou" in text, "Témoignage Abdou S. absent de temoignages.html"
    assert "esn" in text, "Entreprise 'ESN' d'Abdou absente"
    # Vérifier que le bloc témoignage Abdou a un avatar AS
    avatar = page.locator(".author-avatar:has-text('AS')")
    assert avatar.count() >= 1, "Avatar AS d'Abdou absent"


def test_temoignages_page_all_quotes(page, base_url):
    """La page témoignages doit avoir au moins 3 témoignages détaillés."""
    page.goto(f"{base_url}/temoignages.html")
    quotes = page.locator(".testimonial-detail, blockquote")
    assert quotes.count() >= 3, \
        f"Seulement {quotes.count()} témoignages, attendu ≥ 3"


def test_temoignages_page_stars(page, base_url):
    """Chaque témoignage doit avoir des étoiles."""
    page.goto(f"{base_url}/temoignages.html")
    stars = page.locator(".testimonial-detail .stars, .testimonial-detail-header .stars")
    assert stars.count() >= 3, "Étoiles manquantes sur les témoignages"


def test_temoignages_page_stats(page, base_url):
    """La page témoignages doit montrer les chiffres clés."""
    page.goto(f"{base_url}/temoignages.html")
    stats = page.locator(".stat-card, .stat-number")
    assert stats.count() >= 3, "Chiffres clés absents de la page témoignages"


def test_homepage_temoignage_abdou(page, base_url):
    """Le témoignage d'Abdou S. doit aussi apparaître sur l'accueil."""
    page.goto(f"{base_url}/index.html")
    content = page.content().lower()
    assert "abdou" in content, "Témoignage Abdou S. absent de la page d'accueil"


def test_homepage_temoignages_grid(page, base_url):
    """La page d'accueil doit avoir au moins 3 témoignages."""
    page.goto(f"{base_url}/index.html")
    cards = page.locator(".testimonial-card, .testimonials-grid > div")
    assert cards.count() >= 3, \
        f"Seulement {cards.count()} témoignages sur l'accueil, attendu ≥ 3"


# ══════════════════════════════════════════════════════════════
# 6. SECTIONS CLÉS par page
# ══════════════════════════════════════════════════════════════

def test_homepage_sections_completes(page, base_url):
    """L'accueil doit avoir toutes ses sections : hero, formations, coaching, témoignages, CTA."""
    page.goto(f"{base_url}/index.html")
    expect(page.locator(".hero")).to_be_visible()
    assert page.locator(".formations-grid").count() >= 1, "Section formations absente"
    assert page.locator(".testimonials-grid").count() >= 1, "Section témoignages absente"
    assert page.locator(".cta-section").count() >= 1, "Section CTA absente"


def test_formations_sections_completes(page, base_url):
    """La page formations doit avoir ses 3 catégories et le CTA."""
    page.goto(f"{base_url}/formations.html")
    expect(page.locator(".page-header")).to_be_visible()
    assert page.locator(".cta-section").count() >= 1, "Section CTA absente"


def test_coaching_sections_completes(page, base_url):
    """La page coaching doit avoir ses sections clés."""
    page.goto(f"{base_url}/coaching.html")
    expect(page.locator(".page-header")).to_be_visible()
    assert page.locator(".cta-section").count() >= 1, "Section CTA absente"


def test_about_sections_completes(page, base_url):
    """La page à propos doit avoir timeline et certifications."""
    page.goto(f"{base_url}/a-propos.html")
    expect(page.locator(".page-header")).to_be_visible()
    assert page.locator(".timeline").count() >= 1, "Timeline absente"
    assert page.locator(".cta-section").count() >= 1, "Section CTA absente"


def test_faq_sections_completes(page, base_url):
    """La FAQ doit avoir des catégories et le CTA."""
    page.goto(f"{base_url}/faq.html")
    expect(page.locator(".page-header")).to_be_visible()
    categories = page.locator(".faq-category")
    assert categories.count() >= 2, \
        f"Seulement {categories.count()} catégories FAQ, attendu ≥ 2"
    assert page.locator(".cta-section").count() >= 1, "Section CTA absente"


def test_forfait_it_sections_completes(page, base_url):
    """La page forfait-it doit avoir ses sections principales."""
    page.goto(f"{base_url}/forfait-it.html")
    content = page.content()
    assert "forfait" in content.lower(), "Contenu forfait absent"
    assert page.locator(".cta-section, a.btn[href*='contact']").count() >= 1, \
        "CTA contact absent de la page forfait-it"


# ══════════════════════════════════════════════════════════════
# 7. NAVIGATION FONCTIONNELLE — clic et vérification destination
# ══════════════════════════════════════════════════════════════

def test_click_temoignages_from_homepage(page, base_url):
    """Cliquer sur 'Témoignages' dans la nav doit mener à la bonne page."""
    page.goto(f"{base_url}/index.html")
    page.locator("nav a:has-text('moignages')").first.click()
    page.wait_for_load_state("networkidle")
    assert "temoignages" in page.url.lower(), \
        f"Navigation Témoignages mène à '{page.url}'"


def test_click_faq_from_homepage(page, base_url):
    """Cliquer sur 'FAQ' dans la nav doit mener à la bonne page."""
    page.goto(f"{base_url}/index.html")
    page.locator("nav a:has-text('FAQ')").first.click()
    page.wait_for_load_state("networkidle")
    assert "faq" in page.url.lower(), \
        f"Navigation FAQ mène à '{page.url}'"


def test_click_blog_from_homepage(page, base_url):
    """Cliquer sur 'Blog' dans la nav doit mener à la bonne page."""
    page.goto(f"{base_url}/index.html")
    page.locator("nav a:has-text('Blog')").first.click()
    page.wait_for_load_state("networkidle")
    assert "blog" in page.url.lower(), \
        f"Navigation Blog mène à '{page.url}'"


def test_click_contact_from_formations(page, base_url):
    """Depuis formations, le CTA devis doit mener à contact."""
    page.goto(f"{base_url}/formations.html")
    page.locator("a.btn:has-text('devis')").first.click()
    page.wait_for_load_state("networkidle")
    assert "contact" in page.url.lower(), \
        f"CTA devis mène à '{page.url}'"


def test_click_contact_from_coaching(page, base_url):
    """Depuis coaching, le CTA doit mener à contact."""
    page.goto(f"{base_url}/coaching.html")
    page.locator(".cta-section a.btn").first.click()
    page.wait_for_load_state("networkidle")
    assert "contact" in page.url.lower(), \
        f"CTA coaching mène à '{page.url}'"


def test_click_contact_from_temoignages(page, base_url):
    """Depuis témoignages, le CTA doit mener à contact."""
    page.goto(f"{base_url}/temoignages.html")
    page.locator(".cta-section a.btn").first.click()
    page.wait_for_load_state("networkidle")
    assert "contact" in page.url.lower(), \
        f"CTA témoignages mène à '{page.url}'"


# ══════════════════════════════════════════════════════════════
# 8. CONSOLE ERRORS — sur toutes les pages
# ══════════════════════════════════════════════════════════════

ALL_PAGES = [
    "/index.html",
    "/formations.html",
    "/coaching.html",
    "/temoignages.html",
    "/a-propos.html",
    "/faq.html",
    "/blog.html",
    "/contact.html",
    "/forfait-it.html",
    "/lead-magnet.html",
]


@pytest.mark.parametrize("page_path", ALL_PAGES)
def test_no_js_errors_on_page(page, base_url, page_path):
    """Aucune page ne doit avoir d'erreurs JS dans la console."""
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(f"{base_url}{page_path}")
    page.wait_for_load_state("networkidle")
    assert len(errors) == 0, \
        f"Erreurs JS sur {page_path} : {errors}"


@pytest.mark.parametrize("page_path", ALL_PAGES)
def test_no_broken_images_on_page(page, base_url, page_path):
    """Aucune image cassée sur aucune page."""
    page.goto(f"{base_url}{page_path}")
    images = page.locator("img")
    for i in range(images.count()):
        img = images.nth(i)
        src = img.get_attribute("src") or ""
        if src and not src.startswith("data:"):
            natural_width = img.evaluate("el => el.naturalWidth")
            assert natural_width > 0, \
                f"Image cassée sur {page_path} : {src}"
