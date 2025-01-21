import pytest
import requests as req
from playwright.sync_api import Page, expect
from app import Config
from common import logged_page
from tests.models.Registry import RegistryPage

config = Config()


@pytest.mark.default_test
def test_registries(logged_page: Page) -> None:
    registry_page = RegistryPage(logged_page)
    registry_page.navigate()
    expect(logged_page).to_have_url(f"{config.APP_URL}registry/")


@pytest.mark.default_test
def test_count_registries(logged_page: Page) -> None:
    registry_page = RegistryPage(logged_page)
    registry_page.navigate()
    expect(logged_page).to_have_url(f"{config.APP_URL}registry/")
    registries_tabs = registry_page.nav_tabs.all()
    assert len(registries_tabs) <= 1


@pytest.mark.super_user_test
def test_count_registries_super_user(logged_page: Page) -> None:
    registry_page = RegistryPage(logged_page)
    registry_page.navigate()
    expect(logged_page).to_have_url(f"{config.APP_URL}registry/")
    registries_tabs = registry_page.nav_tabs.all()

    if len(config.REGISTRIES) > 1:
        assert len(registries_tabs) > 1
    else:
        assert len(registries_tabs) <= 1


@pytest.mark.default_test
def test_count_repositories(logged_page: Page) -> None:
    registry_page = RegistryPage(logged_page)
    registry_page.navigate()
    expect(logged_page).to_have_url(f"{config.APP_URL}registry/")

    # Pierwsze Registry jest zdefiniowane na ideksie 0, a na stronie od 1 (wynika to z loop.index we Flasku)
    count_of_repositories_on_page = len(get_all_repositories_on_page(registry_page, False))
    count_of_repositories_in_registry = len(get_all_repositories_from_registry(0))

    assert count_of_repositories_on_page == count_of_repositories_in_registry


@pytest.mark.default_test
def test_filter_repositories_by_checkbox(logged_page: Page) -> None:
    registry_page = RegistryPage(logged_page)
    registry_page.navigate()
    expect(logged_page).to_have_url(f"{config.APP_URL}registry/")

    count_of_displayed_repositories_on_page = len(get_all_repositories_on_page(registry_page, True))
    registry_page.show_images_without_tags_checkbox.click()
    count_of_displayed_repositories_on_page_after_filter = len(get_all_repositories_on_page(registry_page, True))

    assert count_of_displayed_repositories_on_page != count_of_displayed_repositories_on_page_after_filter


@pytest.mark.default_test
def test_filter_repositories_by_name(logged_page: Page) -> None:
    registry_page = RegistryPage(logged_page)
    registry_page.navigate()
    expect(logged_page).to_have_url(f"{config.APP_URL}registry/")

    displayed_repositories = get_all_repositories_on_page(registry_page, True)
    count_of_displayed_repositories_on_page = len(displayed_repositories)
    repository_to_check = displayed_repositories[0]
    registry_page.filter_by_name_input.fill(repository_to_check)

    displayed_repositories_after_filter = get_all_repositories_on_page(registry_page, True)
    count_of_displayed_repositories_on_page_after_filter = len(displayed_repositories_after_filter)

    assert count_of_displayed_repositories_on_page_after_filter != count_of_displayed_repositories_on_page

    for repository in displayed_repositories_after_filter:
        assert repository_to_check in repository


@pytest.mark.super_user_test
def test_switching_registry(logged_page: Page) -> None:
    registry_page = RegistryPage(logged_page)
    registry_page.navigate()
    expect(logged_page).to_have_url(f"{config.APP_URL}registry/")

    first_repository_of_first_registry = get_all_repositories_on_page(registry_page, False)[0]
    registry_page.nav_tab_buttons.last.click()
    first_repository_of_second_registry = get_all_repositories_on_page(registry_page, False)[0]

    assert first_repository_of_first_registry != first_repository_of_second_registry


@pytest.mark.count_tags_test
def test_counted_tags(logged_page: Page) -> None:
    registry_page = RegistryPage(logged_page)
    registry_page.navigate()
    expect(logged_page).to_have_url(f"{config.APP_URL}registry/")
    first_repository_name = get_all_repositories_on_page(registry_page, True)[0]
    first_repository_counted_tags = registry_page.displayed_repository_counted_tags_of_active_pane.all_inner_texts()[0]

    count_tags_of_repository = get_repository_tags_from_registry(0, first_repository_name)

    assert int(first_repository_counted_tags) == int(count_tags_of_repository) and count_tags_of_repository > 0


def get_all_repositories_from_registry(registry_index):
    registry = config.REGISTRIES[registry_index]
    url = registry.url
    try:
        response = req.get(url + f"/v2/_catalog?n={Config.PAGINATION_FOR_REQUEST_CATALOG}", auth=(registry.login, registry.password),
                           verify=False).json()['repositories']
    except Exception as e:
        response = []
    return response


def get_repository_tags_from_registry(registry_index, repository):
    registry = config.REGISTRIES[registry_index]
    url = registry.url
    try:
        response = req.get(registry.url + "/v2/" + repository + f"/tags/list?n={Config.PAGINATION_FOR_REQUEST_TAGS_LIST}", auth=(registry.login, registry.password),
                           verify=False)
        if response.status_code == 200:
            list_of_tags = response.json()['tags']
            if list_of_tags is None:
                return 0
            else:
                return len(list_of_tags)
        else:
            return "-1"
    except Exception as e:
        return "-1"


def get_all_repositories_on_page(page, only_displayed: False):
    if only_displayed:
        repository_names = page.displayed_repository_names_of_active_pane.all_inner_texts()
    else:
        repository_names = page.all_repository_names_of_active_pane.all_inner_texts()
    return repository_names

