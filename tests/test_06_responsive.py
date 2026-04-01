"""
Tests de non-régression — Responsive / Mobile.
Vérifie que le site fonctionne sur mobile (375x667 = iPhone SE).
"""
import pytest
from playwright.sync_api import expect


MOBILE_VIEWPORT = {"width": 375, "height": 667}


def test_mobile_navbar_toggle(page, base_url):
    """Sur mobile, le menu burger doit être visible."""
    page.set_viewport_size(MOBILE_VIEWPORT)
    page.goto(f"{base_url}/")
    burger = page.locator(".nav-toggle, .hamburger, button[aria-label='Menu']")
    expect(burger.first).to_be_visible()


def test_mobile_navbar_opens(page, base_url):
    """Cliquer sur le burger doit ouvrir le menu."""
    page.set_viewport_size(MOBILE_VIEWPORT)
    page.goto(f"{base_url}/")
    burger = page.locator(".nav-toggle, .hamburger, button[aria-label='Menu']")
    burger.first.click()
    page.wait_for_timeout(500)
    # Au moins un lien de nav doit devenir visible
    nav_links = page.locator(".nav-links a")
    visible_count = 0
    for i in range(nav_links.count()):
        if nav_links.nth(i).is_visible():
            visible_count += 1
    assert visible_count >= 3, f"Seulement {visible_count} liens visibles après ouverture menu"


def test_mobile_no_horizontal_scroll(page, base_url):
    """Pas de scroll horizontal sur mobile."""
    page.set_viewport_size(MOBILE_VIEWPORT)
    page.goto(f"{base_url}/")
    scroll_width = page.evaluate("document.documentElement.scrollWidth")
    client_width = page.evaluate("document.documentElement.clientWidth")
    assert scroll_width <= client_width + 5, \
        f"Scroll horizontal détecté : {scroll_width} > {client_width}"


def test_mobile_contact_form_usable(page, base_url):
    """Le formulaire contact doit être utilisable sur mobile."""
    page.set_viewport_size(MOBILE_VIEWPORT)
    page.goto(f"{base_url}/contact.html")
    form = page.locator("#contact-form")
    expect(form).to_be_visible()
    submit_btn = page.locator("button[type='submit']")
    expect(submit_btn).to_be_visible()
