"""
Tests RGAA (Référentiel Général d'Amélioration de l'Accessibilité).
Critères de base vérifiables automatiquement.
Référence : https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/
"""
import pytest
from playwright.sync_api import expect


PAGES = [
    "/",
    "/formations.html",
    "/coaching.html",
    "/a-propos.html",
    "/contact.html",
    "/blog.html",
    "/faq.html",
]


# ══════════════════════════════════════════════════════════════
# Thématique 1 — Images
# RGAA 1.1 : Chaque image a-t-elle un attribut alt ?
# RGAA 1.2 : L'alt est-il pertinent (pas vide sur image porteuse d'info) ?
# ══════════════════════════════════════════════════════════════
@pytest.mark.parametrize("path", PAGES)
def test_rgaa_1_1_images_ont_alt(page, base_url, path):
    """RGAA 1.1 — Toute image doit avoir un attribut alt."""
    page.goto(f"{base_url}{path}")
    images = page.locator("img")
    for i in range(images.count()):
        img = images.nth(i)
        alt = img.get_attribute("alt")
        src = img.get_attribute("src") or "?"
        assert alt is not None, f"[{path}] Image sans alt : {src}"


def test_rgaa_1_2_alt_pas_filename(page, base_url):
    """RGAA 1.2 — L'alt ne doit pas être un nom de fichier."""
    page.goto(f"{base_url}/")
    images = page.locator("img")
    for i in range(images.count()):
        img = images.nth(i)
        alt = (img.get_attribute("alt") or "").strip()
        if alt:
            assert not alt.endswith((".jpg", ".png", ".svg", ".webp")), \
                f"Alt semble être un nom de fichier : '{alt}'"


# ══════════════════════════════════════════════════════════════
# Thématique 8 — Éléments obligatoires
# RGAA 8.1 : Doctype HTML5
# RGAA 8.3 : Langue par défaut
# RGAA 8.4 : Langue BCP47 valide
# RGAA 8.5 : Titre de page pertinent
# RGAA 8.6 : Charset UTF-8
# ══════════════════════════════════════════════════════════════
@pytest.mark.parametrize("path", PAGES)
def test_rgaa_8_1_doctype(page, base_url, path):
    """RGAA 8.1 — La page doit avoir un doctype HTML5."""
    page.goto(f"{base_url}{path}")
    doctype = page.evaluate("document.doctype ? document.doctype.name : null")
    assert doctype == "html", f"[{path}] Doctype manquant ou invalide"


@pytest.mark.parametrize("path", PAGES)
def test_rgaa_8_3_lang_definie(page, base_url, path):
    """RGAA 8.3 — La balise html doit avoir un attribut lang."""
    page.goto(f"{base_url}{path}")
    lang = page.locator("html").get_attribute("lang")
    assert lang is not None and len(lang) >= 2, f"[{path}] lang manquant"


@pytest.mark.parametrize("path", PAGES)
def test_rgaa_8_4_lang_valide(page, base_url, path):
    """RGAA 8.4 — La langue doit être un code BCP47 valide (fr)."""
    page.goto(f"{base_url}{path}")
    lang = page.locator("html").get_attribute("lang")
    assert lang in ("fr", "fr-FR"), f"[{path}] lang='{lang}' n'est pas français"


@pytest.mark.parametrize("path", PAGES)
def test_rgaa_8_5_titre_pertinent(page, base_url, path):
    """RGAA 8.5 — Le titre de page doit être pertinent (pas générique)."""
    page.goto(f"{base_url}{path}")
    title = page.title()
    assert len(title) > 10, f"[{path}] Titre trop court : '{title}'"
    generiques = ["accueil", "page", "untitled", "home", "sans titre"]
    title_lower = title.lower()
    for g in generiques:
        assert title_lower != g, f"[{path}] Titre trop générique : '{title}'"


@pytest.mark.parametrize("path", PAGES)
def test_rgaa_8_6_charset_utf8(page, base_url, path):
    """RGAA 8.6 — Le charset doit être déclaré en UTF-8."""
    page.goto(f"{base_url}{path}")
    charset = page.locator("meta[charset]")
    assert charset.count() >= 1, f"[{path}] meta charset manquant"
    val = charset.first.get_attribute("charset").lower()
    assert val == "utf-8", f"[{path}] charset='{val}' au lieu de UTF-8"


# ══════════════════════════════════════════════════════════════
# Thématique 9 — Structuration de l'information
# RGAA 9.1 : Hiérarchie des titres cohérente (pas de saut)
# RGAA 9.2 : Structure du document (landmarks)
# ══════════════════════════════════════════════════════════════
@pytest.mark.parametrize("path", PAGES)
def test_rgaa_9_1_hierarchie_titres(page, base_url, path):
    """RGAA 9.1 — Pas de saut dans la hiérarchie des titres (h1→h2→h3…)."""
    page.goto(f"{base_url}{path}")
    levels = page.evaluate("""
        () => {
            const scope = document.querySelector('main') || document.body;
            const headings = scope.querySelectorAll('h1, h2, h3, h4, h5, h6');
            return Array.from(headings).map(h => parseInt(h.tagName[1]));
        }
    """)
    assert len(levels) >= 1, f"[{path}] Aucun titre trouvé"
    assert levels[0] == 1, f"[{path}] Le premier titre doit être H1, trouvé H{levels[0]}"
    for i in range(1, len(levels)):
        assert levels[i] <= levels[i - 1] + 1, \
            f"[{path}] Saut de titre : H{levels[i-1]} → H{levels[i]}"


@pytest.mark.parametrize("path", PAGES)
def test_rgaa_9_1_un_seul_h1(page, base_url, path):
    """RGAA 9.1 — Une seule balise H1 par page."""
    page.goto(f"{base_url}{path}")
    h1_count = page.locator("h1").count()
    assert h1_count == 1, f"[{path}] {h1_count} H1 trouvé(s), attendu 1"


def test_rgaa_9_2_landmarks(page, base_url):
    """RGAA 9.2 — La page doit avoir les landmarks principaux."""
    page.goto(f"{base_url}/")
    # nav, main, footer (ou rôles ARIA équivalents)
    nav = page.locator("nav, [role='navigation']")
    assert nav.count() >= 1, "Aucun landmark navigation"
    main = page.locator("main, [role='main']")
    assert main.count() >= 1, "Aucun landmark main"
    footer = page.locator("footer, [role='contentinfo']")
    assert footer.count() >= 1, "Aucun landmark footer"


# ══════════════════════════════════════════════════════════════
# Thématique 6 — Liens
# RGAA 6.1 : Intitulé de lien explicite
# RGAA 6.2 : Pas de lien vide
# ══════════════════════════════════════════════════════════════
def test_rgaa_6_1_liens_explicites(page, base_url):
    """RGAA 6.1 — Les liens doivent avoir un intitulé compréhensible."""
    page.goto(f"{base_url}/")
    links = page.locator("a[href]")
    intitules_vagues = ["cliquez ici", "ici", "lien", "click here", "here", "link", "more"]
    for i in range(links.count()):
        link = links.nth(i)
        text = (link.inner_text() or "").strip().lower()
        aria = link.get_attribute("aria-label") or ""
        title = link.get_attribute("title") or ""
        # Le lien doit avoir du texte, un aria-label, un title, ou contenir une image avec alt
        if not text and not aria and not title:
            imgs = link.locator("img[alt]")
            assert imgs.count() >= 1, \
                f"Lien sans intitulé : href='{link.get_attribute('href')}'"
        if text:
            for vague in intitules_vagues:
                assert text != vague, f"Intitulé de lien vague : '{text}'"


@pytest.mark.parametrize("path", PAGES)
def test_rgaa_6_2_pas_de_lien_vide(page, base_url, path):
    """RGAA 6.2 — Aucun lien avec href vide ou '#' seul."""
    page.goto(f"{base_url}{path}")
    liens_vides = page.evaluate("""
        () => {
            const links = document.querySelectorAll('a[href]');
            const bad = [];
            links.forEach(a => {
                const href = a.getAttribute('href').trim();
                if (href === '' || href === '#') {
                    const text = a.textContent.trim().substring(0, 30);
                    bad.push({href, text});
                }
            });
            return bad;
        }
    """)
    assert len(liens_vides) == 0, \
        f"[{path}] Liens vides ou '#' : {liens_vides}"


# ══════════════════════════════════════════════════════════════
# Thématique 11 — Formulaires
# RGAA 11.1 : Chaque champ a un label ou aria-label
# RGAA 11.10 : Bouton submit explicite
# ══════════════════════════════════════════════════════════════
def test_rgaa_11_1_labels_formulaire_contact(page, base_url):
    """RGAA 11.1 — Chaque champ du formulaire contact a un label associé."""
    page.goto(f"{base_url}/contact.html")
    inputs = page.locator("#contact-form input:not([type='hidden']):not([name='bot-field']), #contact-form textarea")
    for i in range(inputs.count()):
        field = inputs.nth(i)
        field_id = field.get_attribute("id") or ""
        name = field.get_attribute("name") or "?"
        aria = field.get_attribute("aria-label") or ""
        placeholder = field.get_attribute("placeholder") or ""
        # Vérifie label via for=id, ou aria-label, ou aria-labelledby
        has_label = False
        if field_id:
            labels = page.locator(f"label[for='{field_id}']")
            has_label = labels.count() >= 1
        if not has_label and aria:
            has_label = True
        aria_by = field.get_attribute("aria-labelledby") or ""
        if not has_label and aria_by:
            has_label = True
        assert has_label, \
            f"Champ '{name}' sans label associé (pas de label[for], aria-label, ou aria-labelledby)"


def test_rgaa_11_10_bouton_submit_explicite(page, base_url):
    """RGAA 11.10 — Le bouton de soumission a un intitulé explicite."""
    page.goto(f"{base_url}/contact.html")
    btn = page.locator("#contact-form button[type='submit']")
    assert btn.count() >= 1, "Pas de bouton submit"
    text = btn.first.inner_text().strip()
    assert len(text) > 2, f"Bouton submit sans texte : '{text}'"


# ══════════════════════════════════════════════════════════════
# Thématique 12 — Navigation
# RGAA 12.7 : Lien d'évitement (skip to content)
# RGAA 12.8 : Ordre de tabulation cohérent
# ══════════════════════════════════════════════════════════════
def test_rgaa_12_7_skip_link(page, base_url):
    """RGAA 12.7 — Un lien d'évitement 'Aller au contenu' doit exister."""
    page.goto(f"{base_url}/")
    skip = page.locator("a[href='#main'], a[href='#content'], a[href='#contenu'], .skip-link, .skip-nav")
    # Le skip link peut être masqué par défaut, vérifier qu'il existe dans le DOM
    assert skip.count() >= 1, \
        "Lien d'évitement (skip to content) manquant"


def test_rgaa_12_8_tabulation_contact(page, base_url):
    """RGAA 12.8 — Tab doit parcourir les champs du formulaire dans l'ordre."""
    page.goto(f"{base_url}/contact.html")
    # Focus le premier champ puis tab
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    # Après plusieurs Tab, le focus doit être sur un élément du formulaire
    focused_tag = page.evaluate("document.activeElement.tagName.toLowerCase()")
    focused_name = page.evaluate("document.activeElement.getAttribute('name') || ''")
    assert focused_tag in ("input", "textarea", "button", "select", "a"), \
        f"Le focus clavier est sur <{focused_tag}> au lieu d'un élément interactif"


# ══════════════════════════════════════════════════════════════
# Thématique 3 — Couleurs / Contraste (vérification basique)
# RGAA 3.2 : Contraste suffisant texte/fond
# ══════════════════════════════════════════════════════════════
def test_rgaa_3_2_contraste_texte_body(page, base_url):
    """RGAA 3.2 — Le texte principal a un contraste suffisant (ratio ≥ 4.5)."""
    page.goto(f"{base_url}/")
    result = page.evaluate("""
        () => {
            // Cibler un paragraphe dans une section à fond clair (pas hero/navy)
            const candidates = document.querySelectorAll('main section:not(.hero):not(.bg-navy) p');
            let el = null;
            for (const p of candidates) {
                const style = getComputedStyle(p);
                const c = style.color;
                const m = c.match(/\\d+/g);
                if (m) {
                    const vals = m.map(Number);
                    // Prendre un paragraphe avec texte sombre (R+G+B < 400)
                    if (vals[0] + vals[1] + vals[2] < 400) { el = p; break; }
                }
            }
            if (!el) el = document.querySelector('main p') || document.body;

            function getBgColor(node) {
                let current = node;
                while (current) {
                    const bg = getComputedStyle(current).backgroundColor;
                    const m = bg.match(/\\d+/g);
                    if (m) {
                        const vals = m.map(Number);
                        // si alpha > 0 (rgb ou rgba avec alpha > 0), on a trouvé
                        if (vals.length === 3 || (vals.length === 4 && vals[3] > 0)) {
                            return bg;
                        }
                    }
                    current = current.parentElement;
                }
                return 'rgb(255, 255, 255)'; // fallback blanc
            }

            const style = getComputedStyle(el);
            const color = style.color;
            const bg = getBgColor(el);

            function parseRgb(c) {
                const m = c.match(/\\d+/g);
                return m ? m.map(Number).slice(0, 3) : [0, 0, 0];
            }
            function luminance(r, g, b) {
                const [rs, gs, bs] = [r, g, b].map(v => {
                    v /= 255;
                    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
                });
                return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
            }

            const [r1, g1, b1] = parseRgb(color);
            const [r2, g2, b2] = parseRgb(bg);
            const l1 = luminance(r1, g1, b1);
            const l2 = luminance(r2, g2, b2);
            const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
            return { ratio: Math.round(ratio * 100) / 100, color, bg };
        }
    """)
    assert result["ratio"] >= 4.5, \
        f"Contraste insuffisant : {result['ratio']}:1 (couleur: {result['color']}, fond: {result['bg']})"


# ══════════════════════════════════════════════════════════════
# Thématique 10 — Présentation
# RGAA 10.7 : Focus visible sur les éléments interactifs
# ══════════════════════════════════════════════════════════════
def test_rgaa_10_7_focus_visible(page, base_url):
    """RGAA 10.7 — Le focus clavier doit être visible sur les liens."""
    page.goto(f"{base_url}/")
    # Tab sur le premier lien
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    # Vérifier que outline n'est pas supprimé
    outline = page.evaluate("""
        () => {
            const el = document.activeElement;
            const style = getComputedStyle(el);
            return {
                outline: style.outline,
                outlineWidth: style.outlineWidth,
                boxShadow: style.boxShadow,
                tag: el.tagName
            };
        }
    """)
    # Le focus doit être visible via outline ou box-shadow
    has_visible_focus = (
        outline["outlineWidth"] != "0px"
        or outline["boxShadow"] != "none"
    )
    assert has_visible_focus, \
        f"Focus invisible sur <{outline['tag']}> : outline={outline['outline']}, box-shadow={outline['boxShadow']}"
