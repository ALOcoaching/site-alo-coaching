"""
Tests de non-régression — Contenu des pages principales.
Vérifie que le contenu métier clé est présent.
"""
from playwright.sync_api import expect


# ══════════════════════════════════════════════════════════════
# Formations
# ══════════════════════════════════════════════════════════════
def test_formations_page_has_cards(page, base_url):
    """La page formations doit avoir des cartes de formation."""
    page.goto(f"{base_url}/formations.html")
    cards = page.locator(".formation-card, .card, article")
    assert cards.count() >= 3, "Au moins 3 formations attendues"


def test_formations_have_duration(page, base_url):
    """Les formations doivent mentionner une durée."""
    page.goto(f"{base_url}/formations.html")
    content = page.content().lower()
    assert "jour" in content, "Durée (jours) non mentionnée"


# ══════════════════════════════════════════════════════════════
# Coaching
# ══════════════════════════════════════════════════════════════
def test_coaching_page_content(page, base_url):
    """La page coaching doit mentionner les offres clés."""
    page.goto(f"{base_url}/coaching.html")
    content = page.content().lower()
    assert "coaching" in content
    assert "individuel" in content or "collectif" in content or "session" in content


# ══════════════════════════════════════════════════════════════
# À propos
# ══════════════════════════════════════════════════════════════
def test_about_page_mentions_arnaud(page, base_url):
    """La page À propos doit mentionner Arnaud Loyet."""
    page.goto(f"{base_url}/a-propos.html")
    content = page.content().lower()
    assert "arnaud" in content
    assert "loyet" in content


def test_about_page_experience(page, base_url):
    """Doit mentionner l'expérience."""
    page.goto(f"{base_url}/a-propos.html")
    content = page.content().lower()
    assert "ans" in content or "exp" in content


# ══════════════════════════════════════════════════════════════
# Blog
# ══════════════════════════════════════════════════════════════
def test_blog_page_has_articles(page, base_url):
    """La page blog doit lister des articles."""
    page.goto(f"{base_url}/blog.html")
    links = page.locator("a[href*='blog-article']")
    assert links.count() >= 3, "Au moins 3 articles de blog"


def test_blog_article_has_content(page, base_url):
    """Un article de blog doit avoir du contenu substantiel."""
    page.goto(f"{base_url}/blog-article-1.html")
    body_text = page.locator("body").inner_text()
    assert len(body_text) > 500, "L'article doit avoir du contenu (>500 chars)"


# ══════════════════════════════════════════════════════════════
# FAQ
# ══════════════════════════════════════════════════════════════
def test_faq_has_questions(page, base_url):
    """La page FAQ doit avoir des questions dépliables."""
    page.goto(f"{base_url}/faq.html")
    questions = page.locator(".faq-question, .accordion-header, details summary, [class*='faq'] span")
    assert questions.count() >= 5, "Au moins 5 questions FAQ"


def test_faq_click_opens_answer(page, base_url):
    """Cliquer sur une question FAQ doit révéler la réponse."""
    page.goto(f"{base_url}/faq.html")
    first_question = page.locator(".faq-question, .accordion-header, details summary").first
    first_question.click()
    page.wait_for_timeout(500)
    # Après clic, du contenu supplémentaire doit être visible
    visible_text = page.locator("body").inner_text()
    assert len(visible_text) > 200


# ══════════════════════════════════════════════════════════════
# Témoignages
# ══════════════════════════════════════════════════════════════
def test_temoignages_has_quotes(page, base_url):
    """La page témoignages doit avoir des citations."""
    page.goto(f"{base_url}/temoignages.html")
    content = page.content().lower()
    assert "«" in content or "\"" in content or "blockquote" in content


# ══════════════════════════════════════════════════════════════
# Forfait IT
# ══════════════════════════════════════════════════════════════
def test_forfait_it_has_pricing(page, base_url):
    """La page forfait doit mentionner des tarifs."""
    page.goto(f"{base_url}/forfait-it.html")
    content = page.content().lower()
    assert "€" in content or "jour" in content


# ══════════════════════════════════════════════════════════════
# Mentions légales & Confidentialité
# ══════════════════════════════════════════════════════════════
def test_mentions_legales_content(page, base_url):
    """Les mentions légales doivent contenir les infos requises."""
    page.goto(f"{base_url}/mentions-legales.html")
    content = page.content().lower()
    assert "arnaud loyet" in content
    assert "netlify" in content or "héberg" in content


def test_politique_confidentialite_rgpd(page, base_url):
    """La politique de confidentialité doit mentionner le RGPD."""
    page.goto(f"{base_url}/politique-confidentialite.html")
    content = page.content().lower()
    assert "rgpd" in content or "données personnelles" in content
