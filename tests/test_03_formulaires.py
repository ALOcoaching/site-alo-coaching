"""
Tests de non-régression — Formulaires (contact + lead-magnet).
Vérifie la structure, les champs requis, la protection spam,
et le comportement après soumission (message FR, pas d'anglais).
"""
import pytest
from playwright.sync_api import expect


# ══════════════════════════════════════════════════════════════
# Formulaire Contact
# ══════════════════════════════════════════════════════════════
def test_contact_form_exists(page, base_url):
    """Le formulaire de contact doit exister et être visible."""
    page.goto(f"{base_url}/contact.html")
    form = page.locator("#contact-form")
    expect(form).to_be_visible()


def test_contact_form_fields(page, base_url):
    """Les champs obligatoires du formulaire contact doivent exister."""
    page.goto(f"{base_url}/contact.html")
    required_fields = ["prenom", "nom", "email", "message"]
    for field_name in required_fields:
        field = page.locator(f"[name='{field_name}']")
        assert field.count() >= 1, f"Champ '{field_name}' manquant"


def test_contact_form_has_netlify_attrs(page, base_url):
    """Le formulaire doit être reconnu par Netlify (champ form-name)."""
    page.goto(f"{base_url}/contact.html")
    form = page.locator("#contact-form")
    # Netlify supprime data-netlify="true" et injecte un champ hidden form-name
    hidden = form.locator("input[name='form-name']")
    assert hidden.count() >= 1, "Champ hidden form-name manquant (Netlify non configuré)"


def test_contact_form_has_action_merci(page, base_url):
    """Le formulaire doit avoir action='/merci.html' (fallback sans JS)."""
    page.goto(f"{base_url}/contact.html")
    form = page.locator("#contact-form")
    action = form.get_attribute("action")
    assert action and "merci" in action.lower(), \
        f"action='{action}' devrait pointer vers merci.html"


def test_contact_form_honeypot(page, base_url):
    """Le champ honeypot anti-spam doit exister mais être caché."""
    page.goto(f"{base_url}/contact.html")
    honeypot = page.locator("[name='bot-field']")
    assert honeypot.count() >= 1, "Champ honeypot manquant"
    assert not honeypot.is_visible(), "Le honeypot ne doit pas être visible"


def test_contact_success_message_fr(page, base_url):
    """Le message de succès doit être en français."""
    page.goto(f"{base_url}/contact.html")
    success_div = page.locator("#form-success")
    html = success_div.inner_html()
    assert "envoy" in html.lower() or "merci" in html.lower(), \
        "Le message de succès doit être en français"
    english_words = ["thank", "success", "submitted", "received"]
    for word in english_words:
        assert word not in html.lower(), f"Texte anglais dans le message de succès : '{word}'"


def test_contact_form_submit_ajax(page, base_url):
    """Soumettre le formulaire contact en AJAX doit afficher le message FR."""
    page.goto(f"{base_url}/contact.html")

    # Intercepter le POST pour ne pas envoyer réellement
    page.route("**/*", lambda route: route.fulfill(status=200, body="OK")
               if route.request.method == "POST" else route.continue_())

    page.fill("[name='prenom']", "Test")
    page.fill("[name='nom']", "Playwright")
    page.fill("[name='email']", "test@test.com")
    page.fill("[name='message']", "Test automatisé")
    page.click("button[type='submit']")

    # le message de succès doit apparaître
    success = page.locator("#form-success")
    expect(success).to_be_visible(timeout=5000)
    assert "envoy" in success.inner_text().lower() or "merci" in success.inner_text().lower()


# ══════════════════════════════════════════════════════════════
# Formulaire Lead Magnet
# ══════════════════════════════════════════════════════════════
def test_leadmagnet_form_exists(page, base_url):
    """Le formulaire lead-magnet doit exister."""
    page.goto(f"{base_url}/lead-magnet.html")
    form = page.locator("#lead-magnet-form")
    expect(form).to_be_visible()


def test_leadmagnet_form_fields(page, base_url):
    """Les champs obligatoires du lead-magnet doivent exister."""
    page.goto(f"{base_url}/lead-magnet.html")
    for field_name in ["firstname", "lastname", "email"]:
        field = page.locator(f"[name='{field_name}']")
        assert field.count() >= 1, f"Champ '{field_name}' manquant"


def test_leadmagnet_form_has_action_merci(page, base_url):
    """Le formulaire lead-magnet doit avoir action='/merci.html'."""
    page.goto(f"{base_url}/lead-magnet.html")
    form = page.locator("#lead-magnet-form")
    action = form.get_attribute("action")
    assert action and "merci" in action.lower(), \
        f"action='{action}' devrait pointer vers merci.html"


def test_leadmagnet_success_message_fr(page, base_url):
    """Le message de succès lead-magnet doit être en français."""
    page.goto(f"{base_url}/lead-magnet.html")
    success_div = page.locator("#lead-form-success")
    html = success_div.inner_html()
    assert "merci" in html.lower() or "pdf" in html.lower()


def test_leadmagnet_form_submit_ajax(page, base_url):
    """Soumettre le lead-magnet en AJAX doit afficher le succès FR."""
    page.goto(f"{base_url}/lead-magnet.html")

    page.route("**/*", lambda route: route.fulfill(status=200, body="OK")
               if route.request.method == "POST" else route.continue_())

    page.fill("[name='firstname']", "Test")
    page.fill("[name='lastname']", "Auto")
    page.fill("[name='email']", "test@test.com")
    page.click("button[type='submit']")

    success = page.locator("#lead-form-success")
    expect(success).to_be_visible(timeout=5000)


# ══════════════════════════════════════════════════════════════
# Page merci.html (fallback)
# ══════════════════════════════════════════════════════════════
def test_merci_page_fr(page, base_url):
    """La page merci.html doit être entièrement en français."""
    page.goto(f"{base_url}/merci.html")
    body_text = page.locator("body").inner_text().lower()
    assert "envoy" in body_text or "merci" in body_text
    english_words = ["thank you", "submission", "received"]
    for word in english_words:
        assert word not in body_text, f"Texte anglais sur merci.html : '{word}'"
