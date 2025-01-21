import re
import urllib.parse

from app import Config

config = Config()


class ImagePage:
    def __init__(self, page):
        self.page = page
        self.repository = page.locator(".card-title")
        self.tag_url = page.locator("#tag-url")
        self.docker_version = page.locator("#docker-version")
        self.os = page.locator("#image-os")
        self.architecture = page.locator("#architecture")
        self.cmd = page.locator("#cmd")
        self.digest = page.locator("#digest")
        self.envs = page.locator(".image-env")
        self.ports = page.locator(".image-port")
        self.repository_name = re.search(r'(?:[^/]+/){3}([^/]+)', page.url).group(1)
        self.registry_name = urllib.parse.unquote(re.search(r'(?:[^/]+/){2}([^/]+)', page.url).group(1))
        self.tag_name = urllib.parse.unquote(re.search(r'(?:[^/]+/){4}([^/]+)', page.url).group(1))
