"""
Configuration Playwright pour les tests ALO Coaching & Formation.
Usage:
  pytest tests/ --base-url=https://aloformationcoaching.netlify.app
  pytest tests/ --base-url=http://localhost:8000   (test local)
"""
import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "locale": "fr-FR",
        "viewport": {"width": 1280, "height": 720},
    }
