import logging
import requests as req
from flask import current_app


def update_registry_access():
    registries = current_app.config['REGISTRIES']
    for registry in registries:
        if registry.name is not current_app.config['SPECIAL_REGISTRY_KEY']:
            try:
                response = req.get(registry.url + "/v2/", auth=(registry.login, registry.password),
                                   verify=False)
                if response.status_code == 200:
                    registry.isAvailable = True
                else:
                    registry.isAvailable = False
            except Exception as e:
                logging.error(e)
