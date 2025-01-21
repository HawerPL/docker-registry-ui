import json
import urllib.parse
import pytest
import requests as req
from datetime import datetime
from playwright.sync_api import expect
from app import Config
from playwright.async_api import Page
from app.routes.registry_routes import get_registry
from tests.models.Login import LoginPage
from tests.models.Registry import RegistryPage
from tests.models.Repository import RepositoryPage

config = Config()


@pytest.fixture
def logged_page(page: Page, request) -> Page:
    login_page = LoginPage(page)
    login_page.navigate()
    if config.SUPER_USER_ENABLED and bool(request.node.get_closest_marker("super_user_test")):
        if config.DEFAULT_LOCALE == "pl":
            all_registries = "Wszystkie rejestry"
        else:
            all_registries = "All registries"
        login_page.login(config.SUPER_USER_LOGIN, config.SUPER_USER_PASSWORD, all_registries)
    else:
        login_page.login(config.REGISTRIES[0].login, config.REGISTRIES[0].password,
                         f"{config.REGISTRIES[0].name} ({config.REGISTRIES[0].url})")
    expect(page).to_have_url(config.APP_URL)
    return page


@pytest.fixture
def registry_page(logged_page: Page, request) -> Page:
    registry_page = RegistryPage(logged_page)
    registry_page.navigate()
    expect(logged_page).to_have_url(f"{config.APP_URL}registry/")
    return logged_page


@pytest.fixture
def repository_page(registry_page: Page, request) -> Page:
    index_repository = 0
    repository_page = RegistryPage(registry_page)
    registry_name_decoded = urllib.parse.quote(repository_page.registry_name[0])
    repository_name = repository_page.displayed_repository_names_of_active_pane.all()[index_repository].inner_text()
    repository_page.navigate_to_repository(index_repository)
    expect(registry_page).to_have_url(f"{config.APP_URL}registry/{registry_name_decoded}/{repository_name}/tags")
    return registry_page


@pytest.fixture
def image_page(repository_page: Page, request) -> Page:
    index_image = 0
    image_page = RepositoryPage(repository_page)
    registry_name_decoded = urllib.parse.quote(image_page.registry_name)
    repository_name_decoded = urllib.parse.quote(image_page.repository_name)
    tag_name = image_page.displayed_tags.all()[index_image].inner_text()
    image_page.navigate_to_image(index_image)
    expect(repository_page).to_have_url(f"{config.APP_URL}registry/{registry_name_decoded}/{repository_name_decoded}/"
                                        f"{tag_name}")
    return repository_page


def get_manifest(registry_name, repository, image_tag):
    registry = get_registry_test(registry_name)
    manifest = get_image_manifest(repository, registry, image_tag,
                                  "application/vnd.docker.distribution.manifest.list.v2+json")
    manifest.update(get_image_manifest(repository, registry, image_tag,
                                       "application/vnd.docker.distribution.manifest.v2+json"))

    v1_compatibility = json.loads(manifest['history'][0]['v1Compatibility'])

    v1_compatibility['created'] = docker_date_to_datetime(v1_compatibility['created'])
    manifest['created'] = {"created": v1_compatibility['created']}
    return manifest


def get_image_manifest(repository, registry, tag, application_header):
    url = registry.url
    details = {}
    headers = {'Accept': f'{application_header}'}
    try:
        response = req.get(url + "/v2/" + repository + "/manifests/" + tag,
                           auth=(registry.login, registry.password), verify=False, headers=headers)
        details = response.json()
        details['tag_digest'] = response.headers['Docker-Content-Digest']
    except Exception as e:
        details = {}
    return details


def docker_date_to_datetime(docker_date):
    docker_data_format = '%Y-%m-%dT%H:%M:%S.%f'
    data_string = docker_date
    microseconds = int(data_string.split(".")[1][:6])
    data_string = data_string.replace(data_string.split(".")[1], str(microseconds).zfill(6))
    new_format = '%Y-%m-%d %H:%M:%S'
    return datetime.strptime(data_string, docker_data_format).strftime(new_format)


def get_registry_test(registry_name):
    return next((reg for reg in Config.REGISTRIES if reg.name == registry_name), None)


def get_all_tags(registry_name, repository):
    registry = get_registry_test(registry_name)
    url = registry.url
    try:
        response = req.get(url + "/v2/" + repository + f"/tags/list?n={Config.PAGINATION_FOR_REQUEST_TAGS_LIST}",
                           auth=(registry.login, registry.password), verify=False).json()['tags']
    except Exception as e:
        response = []
    return response