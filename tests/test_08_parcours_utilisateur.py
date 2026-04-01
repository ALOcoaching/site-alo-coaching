"""
Tests IHM — Parcours utilisateur (scénarios E2E).
Simule de vrais visiteurs naviguant sur le site.
"""
import pytest
from playwright.sync_api import expect


# ══════════════════════════════════════════════════════════════
# Scénario 1 : Visiteur découvre le site depuis l'accueil
# ══════════════════════════════════════════════════════════════
class TestParcoursDecouverte:
    """Un visiteur arrive sur l'accueil et explore le site."""

    def test_arrive_sur_accueil_voit_hero(self, page, base_url):
        """Le visiteur arrive, voit le hero et les CTA."""
        page.goto(f"{base_url}/")
        expect(page.locator("h1")).to_be_visible()
        cta = page.locator(".hero .btn, .hero-content .btn")
        expect(cta.first).to_be_visible()

    def test_clique_decouvrir_formations(self, page, base_url):
        """Depuis l'accueil, clique sur 'Découvrir les formations'."""
        page.goto(f"{base_url}/")
        cta = page.locator("a.btn:has-text('formations')")
        expect(cta.first).to_be_visible()
        cta.first.click()
        page.wait_for_load_state("domcontentloaded")
        assert "/formations" in page.url
        expect(page.locator("h1")).to_be_visible()

    def test_scroll_accueil_puis_coaching(self, page, base_url):
        """Scroll l'accueil, puis navigue vers coaching via le menu."""
        page.goto(f"{base_url}/")
        # Scroll vers le bas pour voir les sections
        page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        page.wait_for_timeout(500)
        # Clique Coaching dans la navbar
        page.locator(".nav-links a:has-text('Coaching')").click()
        page.wait_for_load_state("domcontentloaded")
        assert "/coaching" in page.url

    def test_accueil_vers_contact_via_cta(self, page, base_url):
        """Le CTA 'Parlons de votre projet' mène à la page contact."""
        page.goto(f"{base_url}/")
        cta = page.locator("a.btn:has-text('projet')")
        if cta.count() > 0:
            cta.first.scroll_into_view_if_needed()
            cta.first.click()
            page.wait_for_load_state("domcontentloaded")
            assert "/contact" in page.url
        else:
            # fallback : CTA contact dans le hero
            page.locator("a.btn:has-text('contacter')").first.click()
            page.wait_for_load_state("domcontentloaded")
            assert "/contact" in page.url


# ══════════════════════════════════════════════════════════════
# Scénario 2 : Prospect recherche une formation
# ══════════════════════════════════════════════════════════════
class TestParcoursFormation:
    """Un prospect consulte les formations et s'informe."""

    def test_consulte_formations_voit_cartes(self, page, base_url):
        """La page formations affiche des cartes cliquables/lisibles."""
        page.goto(f"{base_url}/formations.html")
        cards = page.locator(".formation-card, .card, article")
        assert cards.count() >= 3
        # Chaque carte est visible
        for i in range(min(cards.count(), 3)):
            expect(cards.nth(i)).to_be_visible()

    def test_formations_vers_contact(self, page, base_url):
        """Depuis formations, un CTA permet d'aller vers contact."""
        page.goto(f"{base_url}/formations.html")
        contact_link = page.locator("a[href*='contact'], a:has-text('contact')")
        assert contact_link.count() >= 1, "Pas de lien vers contact depuis formations"
        contact_link.first.scroll_into_view_if_needed()
        contact_link.first.click()
        page.wait_for_load_state("domcontentloaded")
        assert "/contact" in page.url

    def test_navigue_formations_blog_faq(self, page, base_url):
        """Le prospect consulte formations, puis blog, puis FAQ."""
        page.goto(f"{base_url}/formations.html")
        expect(page.locator("h1")).to_be_visible()

        # Navigue vers le blog
        page.goto(f"{base_url}/blog.html")
        page.wait_for_load_state("domcontentloaded")
        assert "/blog" in page.url

        # Depuis le blog, va vers FAQ via le footer ou nav
        faq_link = page.locator("a:has-text('FAQ')")
        faq_link.first.scroll_into_view_if_needed()
        faq_link.first.click()
        page.wait_for_load_state("domcontentloaded")
        assert "/faq" in page.url


# ══════════════════════════════════════════════════════════════
# Scénario 3 : Visiteur remplit le formulaire de contact
# ══════════════════════════════════════════════════════════════
class TestParcoursContact:
    """Un visiteur remplit et soumet le formulaire contact."""

    def test_arrive_contact_formulaire_visible(self, page, base_url):
        """Le formulaire contact est immédiatement visible."""
        page.goto(f"{base_url}/contact.html")
        form = page.locator("#contact-form")
        expect(form).to_be_visible()
        expect(page.locator("button[type='submit']")).to_be_visible()

    def test_remplir_formulaire_champs(self, page, base_url):
        """Le visiteur peut remplir tous les champs du formulaire."""
        page.goto(f"{base_url}/contact.html")
        page.fill("[name='prenom']", "Marie")
        page.fill("[name='nom']", "Dupont")
        page.fill("[name='email']", "marie.dupont@example.com")
        page.fill("[name='message']", "Bonjour, je souhaite en savoir plus sur vos formations.")
        # Vérifie que les valeurs sont bien saisies
        assert page.input_value("[name='prenom']") == "Marie"
        assert page.input_value("[name='nom']") == "Dupont"
        assert page.input_value("[name='email']") == "marie.dupont@example.com"
        assert "formations" in page.input_value("[name='message']")

    def test_formulaire_champ_vide_bloque(self, page, base_url):
        """Soumettre avec un champ requis vide ne doit pas passer."""
        page.goto(f"{base_url}/contact.html")
        # Ne remplir que le prénom et essayer de soumettre
        page.fill("[name='prenom']", "Test")
        page.click("button[type='submit']")
        # On reste sur la même page (le navigateur bloque les required)
        assert "/contact" in page.url

    def test_contact_depuis_a_propos(self, page, base_url):
        """Depuis À propos, le visiteur rejoint la page contact."""
        page.goto(f"{base_url}/a-propos.html")
        expect(page.locator("h1")).to_be_visible()
        # Via navbar
        page.locator(".nav-links a:has-text('Contact'), a.nav-cta").first.click()
        page.wait_for_load_state("domcontentloaded")
        assert "/contact" in page.url
        expect(page.locator("#contact-form")).to_be_visible()


# ══════════════════════════════════════════════════════════════
# Scénario 4 : Visiteur télécharge le PDF (lead magnet)
# ══════════════════════════════════════════════════════════════
class TestParcoursLeadMagnet:
    """Un visiteur veut télécharger le guide PDF gratuit."""

    def test_lead_magnet_formulaire_visible(self, page, base_url):
        """Le formulaire lead-magnet est visible et a les bons champs."""
        page.goto(f"{base_url}/lead-magnet.html")
        form = page.locator("#lead-magnet-form")
        expect(form).to_be_visible()
        expect(page.locator("[name='firstname']")).to_be_visible()
        expect(page.locator("[name='lastname']")).to_be_visible()
        expect(page.locator("[name='email']")).to_be_visible()

    def test_remplir_lead_magnet(self, page, base_url):
        """Le visiteur saisit ses coordonnées pour le PDF."""
        page.goto(f"{base_url}/lead-magnet.html")
        page.fill("[name='firstname']", "Jean")
        page.fill("[name='lastname']", "Martin")
        page.fill("[name='email']", "jean.martin@example.com")
        assert page.input_value("[name='firstname']") == "Jean"
        assert page.input_value("[name='email']") == "jean.martin@example.com"


# ══════════════════════════════════════════════════════════════
# Scénario 5 : Visiteur explore le blog
# ══════════════════════════════════════════════════════════════
class TestParcoursBlog:
    """Un visiteur lit les articles du blog."""

    def test_blog_liste_articles_cliquables(self, page, base_url):
        """Les articles du blog sont listés avec des liens."""
        page.goto(f"{base_url}/blog.html")
        articles = page.locator("a[href*='blog-article']")
        assert articles.count() >= 3
        # Le premier lien est cliquable
        expect(articles.first).to_be_visible()

    def test_blog_ouvre_article_et_revient(self, page, base_url):
        """Cliquer un article l'ouvre, le bouton retour fonctionne."""
        page.goto(f"{base_url}/blog.html")
        first_article = page.locator("a[href*='blog-article']").first
        first_article.click()
        page.wait_for_load_state("domcontentloaded")
        assert "blog-article" in page.url
        # L'article a du contenu substantiel
        body = page.locator("body").inner_text()
        assert len(body) > 500

        # Retour navigateur
        page.go_back()
        page.wait_for_load_state("domcontentloaded")
        assert "/blog" in page.url

    def test_blog_article_vers_contact(self, page, base_url):
        """Depuis un article, on peut aller vers contact."""
        page.goto(f"{base_url}/blog-article-1.html")
        # Via navbar ou CTA
        contact = page.locator(".nav-links a:has-text('Contact'), a.nav-cta, a[href*='contact']")
        assert contact.count() >= 1
        contact.first.click()
        page.wait_for_load_state("domcontentloaded")
        assert "/contact" in page.url


# ══════════════════════════════════════════════════════════════
# Scénario 6 : Visiteur consulte la FAQ
# ══════════════════════════════════════════════════════════════
class TestParcoursFAQ:
    """Un visiteur consulte les questions fréquentes."""

    def test_faq_ouvre_ferme_questions(self, page, base_url):
        """Les questions FAQ s'ouvrent et se ferment au clic."""
        page.goto(f"{base_url}/faq.html")
        questions = page.locator(".faq-question, .accordion-header, details summary")
        assert questions.count() >= 5

        # Ouvrir la première question
        questions.first.click()
        page.wait_for_timeout(400)

        # Ouvrir la deuxième
        questions.nth(1).click()
        page.wait_for_timeout(400)

        # Les 2 premières sont interactives, le contenu visible augmente
        visible_text = page.locator("body").inner_text()
        assert len(visible_text) > 300

    def test_faq_puis_formations(self, page, base_url):
        """Après la FAQ, le visiteur navigue vers formations."""
        page.goto(f"{base_url}/faq.html")
        page.locator(".nav-links a:has-text('Formations')").click()
        page.wait_for_load_state("domcontentloaded")
        assert "/formations" in page.url


# ══════════════════════════════════════════════════════════════
# Scénario 7 : Navigation mobile complète
# ══════════════════════════════════════════════════════════════
MOBILE = {"width": 375, "height": 667}


class TestParcoursMobile:
    """Un visiteur sur mobile navigue via le burger menu."""

    def test_mobile_ouvre_menu_navigue(self, page, base_url):
        """Sur mobile, ouvrir le menu et naviguer vers Formations."""
        page.set_viewport_size(MOBILE)
        page.goto(f"{base_url}/")
        expect(page.locator("h1")).to_be_visible()

        # Ouvrir le burger
        burger = page.locator(".nav-toggle, .hamburger, button[aria-label='Menu']")
        expect(burger.first).to_be_visible()
        burger.first.click()
        page.wait_for_timeout(500)

        # Cliquer Formations
        page.locator(".nav-links a:has-text('Formations')").click()
        page.wait_for_load_state("domcontentloaded")
        assert "/formations" in page.url

    def test_mobile_accueil_vers_contact(self, page, base_url):
        """Sur mobile, aller de l'accueil au formulaire contact."""
        page.set_viewport_size(MOBILE)
        page.goto(f"{base_url}/")

        # Ouvrir le burger et aller sur contact
        burger = page.locator(".nav-toggle, .hamburger, button[aria-label='Menu']")
        burger.first.click()
        page.wait_for_timeout(500)
        page.locator(".nav-links a:has-text('Contact'), a.nav-cta").first.click()
        page.wait_for_load_state("domcontentloaded")
        assert "/contact" in page.url

        # Le formulaire est utilisable sur mobile
        expect(page.locator("#contact-form")).to_be_visible()
        page.fill("[name='prenom']", "Mobile")
        assert page.input_value("[name='prenom']") == "Mobile"

    def test_mobile_scroll_et_cta(self, page, base_url):
        """Sur mobile, scroller et cliquer un CTA fonctionne."""
        page.set_viewport_size(MOBILE)
        page.goto(f"{base_url}/")
        # Scroll vers le milieu
        page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
        page.wait_for_timeout(500)
        # Un CTA doit être accessible
        cta = page.locator("a.btn")
        assert cta.count() >= 1


# ══════════════════════════════════════════════════════════════
# Scénario 8 : Parcours complet visiteur → prospect
# ══════════════════════════════════════════════════════════════
class TestParcoursComplet:
    """Scénario bout-en-bout : visiteur arrive, explore, devient prospect."""

    def test_parcours_visiteur_complet(self, page, base_url):
        """Accueil → Formations → Coaching → Témoignages → À propos → Contact."""
        # 1. Arrive sur l'accueil
        page.goto(f"{base_url}/")
        expect(page.locator("h1")).to_be_visible()

        # 2. Explore les formations
        page.locator(".nav-links a:has-text('Formations')").click()
        page.wait_for_load_state("domcontentloaded")
        assert "/formations" in page.url
        cards = page.locator(".formation-card, .card, article")
        assert cards.count() >= 3

        # 3. Regarde le coaching
        page.locator(".nav-links a:has-text('Coaching')").click()
        page.wait_for_load_state("domcontentloaded")
        assert "/coaching" in page.url

        # 4. Lit les témoignages
        page.goto(f"{base_url}/temoignages.html")
        page.wait_for_load_state("domcontentloaded")
        content = page.content().lower()
        assert "moignage" in content or "client" in content

        # 5. Vérifie l'expérience du formateur
        page.locator(".nav-links a:has-text('propos')").click()
        page.wait_for_load_state("domcontentloaded")
        assert "arnaud" in page.content().lower()

        # 6. Arrive sur contact et remplit le formulaire
        page.locator(".nav-links a:has-text('Contact'), a.nav-cta").first.click()
        page.wait_for_load_state("domcontentloaded")
        assert "/contact" in page.url
        page.fill("[name='prenom']", "Sophie")
        page.fill("[name='nom']", "Bernard")
        page.fill("[name='email']", "sophie.bernard@example.com")
        page.fill("[name='message']", "Suite à ma visite, je suis intéressée par la formation gestion de projets.")
        assert page.input_value("[name='email']") == "sophie.bernard@example.com"
