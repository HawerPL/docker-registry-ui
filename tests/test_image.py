import json
import pytest
from playwright.sync_api import Page
from app import Config
from common import image_page, repository_page, get_manifest

from tests.models.Image import ImagePage

config = Config()


@pytest.mark.default_test
def test_image(image_page: Page) -> None:
    image_page = ImagePage(image_page)


@pytest.mark.default_test
def test_image_info(image_page: Page) -> None:
    image_page = ImagePage(image_page)
    tag_manifest_in_registry = get_manifest(image_page.registry_name, image_page.repository_name, image_page.tag_name)
    v1_compatibility = json.loads(tag_manifest_in_registry['history'][0]['v1Compatibility'])
    assert image_page.digest.inner_text() == tag_manifest_in_registry['config']['digest']
    assert image_page.os.inner_text() == v1_compatibility['os']
    assert image_page.architecture.inner_text() == tag_manifest_in_registry['architecture']
    assert image_page.docker_version.inner_text() == v1_compatibility['docker_version']
    assert image_page.repository.inner_text() == f"REPOZYTORIUM: {tag_manifest_in_registry['name']}"
    assert image_page.cmd.inner_text() == str(v1_compatibility['config']['Cmd'])


