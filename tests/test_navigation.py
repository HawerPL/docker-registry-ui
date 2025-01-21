import pytest
from playwright.sync_api import Page, expect
from app import Config
from common import logged_page
from tests.models.Navigation import NavigationPage

config = Config()


@pytest.mark.default_test
def test_home(logged_page: Page) -> None:
    navigation_page = NavigationPage(logged_page)
    navigation_page.navigate()
    navigation_page.registry_explorer_button.click()
    expect(logged_page).to_have_url(f"{config.APP_URL}registry/")
    navigation_page.home_button.click()
    expect(logged_page).to_have_url(f"{config.APP_URL}")


@pytest.mark.default_test
def test_registry_explorer(logged_page: Page) -> None:
    navigation_page = NavigationPage(logged_page)
    navigation_page.navigate()
    navigation_page.home_button.click()
    expect(logged_page).to_have_url(f"{config.APP_URL}")
    navigation_page.registry_explorer_button.click()
    expect(logged_page).to_have_url(f"{config.APP_URL}registry/")


@pytest.mark.default_test
def test_language(logged_page: Page) -> None:
    navigation_page = NavigationPage(logged_page)
    navigation_page.navigate()
    navigation_page.polish_button.click()
    expect(navigation_page.registry_explorer_button).to_have_text("Przeglądarka rejestrów")
    navigation_page.english_button.click()
    expect(navigation_page.registry_explorer_button).to_have_text("Registry explorer")
    navigation_page.polish_button.click()
    expect(navigation_page.registry_explorer_button).to_have_text("Przeglądarka rejestrów")


@pytest.mark.default_test
def test_theme(logged_page: Page) -> None:
    navigation_page = NavigationPage(logged_page)
    navigation_page.navigate()
    navigation_page.dark_theme_button.click()
    expect(navigation_page.html_tag).to_have_attribute("data-bs-theme", "dark")
    navigation_page.light_theme_button.click()
    expect(navigation_page.html_tag).to_have_attribute("data-bs-theme", "light")
    navigation_page.dark_theme_button.click()
    expect(navigation_page.html_tag).to_have_attribute("data-bs-theme", "dark")


@pytest.mark.default_test
def test_logout(logged_page: Page) -> None:
    navigation_page = NavigationPage(logged_page)
    navigation_page.navigate()
    navigation_page.logout_button.click()
    expect(logged_page).to_have_url(f"{config.APP_URL}login")
