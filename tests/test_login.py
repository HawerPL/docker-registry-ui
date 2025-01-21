import pytest
from playwright.sync_api import Page, expect
from app import Config
from tests.models.Login import LoginPage

config = Config()


@pytest.mark.default_test
def test_login(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(config.REGISTRIES[0].login, config.REGISTRIES[0].password,
                     f"{config.REGISTRIES[0].name} ({config.REGISTRIES[0].url})")
    expect(page).to_have_url(config.APP_URL)


@pytest.mark.default_test
def test_login_wrong_username(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("qwertyuiop", config.REGISTRIES[0].password,
                     f"{config.REGISTRIES[0].name} ({config.REGISTRIES[0].url})")
    expect(page).to_have_url(f"{config.APP_URL}login")


@pytest.mark.default_test
def test_login_wrong_password(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(config.REGISTRIES[0].login, "qwertyuiop",
                     f"{config.REGISTRIES[0].name} ({config.REGISTRIES[0].url})")
    expect(page).to_have_url(f"{config.APP_URL}login")


@pytest.mark.default_test
def test_login_wrong_registry(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(config.REGISTRIES[0].login, config.REGISTRIES[0].password,
                     f"{config.REGISTRIES[1].name} ({config.REGISTRIES[1].url})")
    expect(page).to_have_url(f"{config.APP_URL}login")


@pytest.mark.super_user_test
def test_login_super_user(page: Page) -> None:
    login_page = LoginPage(page)
    login_page.navigate()
    if config.DEFAULT_LOCALE == "pl":
        all_registries = "Wszystkie rejestry"
    else:
        all_registries = "All registries"
    login_page.login(config.SUPER_USER_LOGIN, config.SUPER_USER_PASSWORD, all_registries)
    expect(page).to_have_url(config.APP_URL)

