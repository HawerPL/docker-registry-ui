import pytest
from common import logged_page, registry_page, repository_page, image_page
from playwright.async_api import Page

from app import Config
from tests.models.Login import LoginPage


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "default_test"
    )

    if Config.SUPER_USER_ENABLED:
        config.addinivalue_line(
            "markers", "super_user_test"
        )
    if Config.COUNT_TAGS:
        config.addinivalue_line(
            "markers", "count_tags_test"
        )
    if Config.MINIMAL_REPOSITORY_INFO:
        config.addinivalue_line(
            "markers", "minimal_repository_info_test"
        )


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

