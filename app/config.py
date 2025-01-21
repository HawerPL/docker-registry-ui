import os
import logging
import random
import string

from flask import current_app

from app.models.registry import Registry
from app.models.user import User, users


def update_special_registry_key():
    chars = string.ascii_uppercase + string.digits
    current_app.config['SPECIAL_REGISTRY_KEY'] = ''.join(random.choice(chars) for _ in range(16))


class Config(object):

    url_registries = [value for key, value in os.environ.items() if key.startswith('DOCKER_REGISTRY_URL_')]

    COUNT_OF_REGISTRIES = len(url_registries)
    REGISTRIES = []

    SPECIAL_REGISTRY_KEY = "TEST_REGISTRY_KEY"

    SUPER_USER_ENABLED = os.environ.get("SUPER_USER_ENABLED", 'False').lower() in ('true', '1', 't')
    SUPER_USER_LOGIN = None
    SUPER_USER_PASSWORD = None

    if SUPER_USER_ENABLED:
        
        SUPER_USER_LOGIN = os.environ.get("SUPER_USER_LOGIN")
        SUPER_USER_PASSWORD = os.environ.get("SUPER_USER_PASSWORD")

        users.append(User(len(users) + 1, SUPER_USER_LOGIN, SUPER_USER_PASSWORD))

    for i in range(1, COUNT_OF_REGISTRIES + 1):
        registry_url = os.environ.get(f"DOCKER_REGISTRY_URL_{i}")
        registry_name = os.environ.get(f"DOCKER_REGISTRY_NAME_{i}")
        registry_login = os.environ.get(f"DOCKER_REGISTRY_LOGIN_{i}")
        registry_password = os.environ.get(f"DOCKER_REGISTRY_PASSWORD_{i}")
        registry_is_deletable = (os.environ.get(f"DOCKER_REGISTRY_IS_DELETABLE_{i}", 'False').lower() in
                                 ('true', '1', 't'))
        registry = Registry(registry_name, registry_login, registry_password, registry_url, registry_is_deletable)
        REGISTRIES.append(registry)

        users.append(User(len(users) + 1, registry_login, registry_password, registry))

    APP_NAME = os.environ.get("APP_NAME")
    LOG_LEVEL = getattr(logging, os.environ.get('LOG_LEVEL', 'INFO').upper(), logging.DEBUG)
    SESSION_TIME = int(os.environ.get("SESSION_TIME", 60))
    DEFAULT_LOCALE = os.environ.get("DEFAULT_LOCALE", 'pl')
    ENABLED_AUTH = os.environ.get("ENABLED_AUTH", 'False').lower() in ('true', '1', 't')
    # Required mapped volume
    ENABLED_LOGO = os.environ.get("ENABLED_LOGO", 'False').lower() in ('true', '1', 't')
    COUNT_TAGS = os.environ.get("COUNT_TAGS", 'False').lower() in ('true', '1', 't')
    MINIMAL_REPOSITORY_INFO = os.environ.get("MINIMAL_REPOSITORY_INFO", 'True').lower() in ('true', '1', 't')
    PAGINATION_FOR_REQUEST_CATALOG = int(os.environ.get("PAGINATION_FOR_REQUEST_CATALOG", 1000))
    PAGINATION_FOR_REQUEST_TAGS_LIST = int(os.environ.get("PAGINATION_FOR_REQUEST_TAGS_LIST", 1000))

    ENABLE_EDIT_TAG = False

    # Config for tests
    APP_URL = os.environ.get("APP_URL")





