import pytest
from playwright.sync_api import Page
from app import Config
from common import repository_page, get_all_tags, get_manifest
from tests.models.Repository import RepositoryPage

config = Config()


@pytest.mark.default_test
def test_repository(repository_page: Page) -> None:
    repository_page = RepositoryPage(repository_page)
    count_tags_in_registry = len(get_all_tags(repository_page.registry_name, repository_page.repository_name))
    count_tags_on_page = len(repository_page.get_all_tags_on_page(False))
    assert count_tags_on_page == count_tags_in_registry


@pytest.mark.default_test
def test_filter_by_name(repository_page: Page) -> None:
    repository_page = RepositoryPage(repository_page)
    displayed_tags = repository_page.get_all_tags_on_page(True)
    count_tags_on_page = len(displayed_tags)
    tag_to_check = displayed_tags[0]

    if count_tags_on_page == 1:
        repository_page.filter_by_name_input.fill("afjoiswafhoiwesh fqwe09ru9023rh")
        displayed_tags_after_filter = repository_page.get_all_tags_on_page(True)
        count_tags_on_page_after_filter = len(displayed_tags_after_filter)
        assert count_tags_on_page_after_filter == 0
    else:
        repository_page.filter_by_name_input.fill(tag_to_check)
        displayed_tags_after_filter = repository_page.get_all_tags_on_page(True)
        count_tags_on_page_after_filter = len(displayed_tags_after_filter)
        assert count_tags_on_page_after_filter < count_tags_on_page


@pytest.mark.minimal_repository_info_test
def test_compare_docker_content_digest(repository_page: Page) -> None:
    checked_index = 0
    repository_page = RepositoryPage(repository_page)
    displayed_tags = repository_page.get_all_tags_on_page(True)
    tag_to_check = displayed_tags[checked_index]
    tag_manifest_in_registry = get_manifest(repository_page.registry_name, repository_page.repository_name, tag_to_check)
    displayed_docker_content_digest = repository_page.get_all_docker_content_digest_on_page(True)
    assert displayed_docker_content_digest[checked_index] == tag_manifest_in_registry['config']['digest']


@pytest.mark.minimal_repository_info_test
def test_compare_architecture(repository_page: Page) -> None:
    checked_index = 0
    repository_page = RepositoryPage(repository_page)
    displayed_tags = repository_page.get_all_tags_on_page(True)
    tag_to_check = displayed_tags[checked_index]
    tag_manifest_in_registry = get_manifest(repository_page.registry_name, repository_page.repository_name,
                                            tag_to_check)
    displayed_architecture = repository_page.get_all_architecture_on_page(True)
    assert displayed_architecture[checked_index] == tag_manifest_in_registry['architecture']


@pytest.mark.minimal_repository_info_test
def test_compare_size(repository_page: Page) -> None:
    checked_index = 0
    repository_page = RepositoryPage(repository_page)
    displayed_tags = repository_page.get_all_tags_on_page(True)
    tag_to_check = displayed_tags[checked_index]
    tag_manifest_in_registry = get_manifest(repository_page.registry_name, repository_page.repository_name,
                                            tag_to_check)
    displayed_size = repository_page.get_all_size_on_page(True)
    assert int(displayed_size[checked_index]) == tag_manifest_in_registry['layers'][0]['size']
