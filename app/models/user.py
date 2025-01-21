from flask_login import UserMixin
import requests as req
import logging

users = []


class User(UserMixin):
    def __init__(self, user_id, username, password, registry=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.registry = registry

    def __str__(self):
        return f"User(id={self.user_id}, login={self.username}, password=***)"

    def get_id(self):
        return self.user_id


def is_authorized(username, password, registry_url):
    try:
        response = req.get(registry_url + "/v2/", auth=(username, password),
                           verify=False)
        if response.status_code == 401:
            return 401
        else:
            return 200
    except Exception as e:
        logging.error(e)
    return 400


def is_superuser(username, password, super_user_username, super_user_password):
    if super_user_password == password and super_user_username == username:
        return True
    else:
        return False
