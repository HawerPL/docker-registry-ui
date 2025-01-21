import re
import urllib.parse
from app import Config

config = Config()


class RepositoryPage:
    def __init__(self, page):
        self.page = page
        self.filter_by_name_input = page.locator("#tags-search")
        self.all_repository_names_of_active_pane = (
            page.locator(f".active > table > tbody > .repository-row > td > .repository-name"))
        self.displayed_repository_names_of_active_pane = (
            page.locator(f".active > table > tbody > .repository-row.d-table-row > td > .repository-name"))
        self.displayed_tags = (
            page.locator(f"table > tbody > .tag-row.d-table-row > td > .tag-name"))
        self.repository_name = re.search(r'(?:[^/]+/){3}([^/]+)', page.url).group(1)
        self.registry_name = urllib.parse.unquote(re.search(r'(?:[^/]+/){2}([^/]+)', page.url).group(1))

    def navigate(self, child):
        self.displayed_repository_names_of_active_pane[child].click()

    def navigate_to_image(self, child):
        self.displayed_tags.all()[child].click()

    def get_all_tags_on_page(self, only_displayed: False):
        if only_displayed:
            tags_names = self.page.locator(".d-table-row .tag-name").all_inner_texts()
        else:
            tags_names = self.page.locator(".tag-name").all_inner_texts()
        return tags_names

    def get_all_docker_content_digest_on_page(self, only_displayed: False):
        if only_displayed:
            dcds = self.page.locator(".d-table-row .docker-contest-digest").all_inner_texts()
        else:
            dcds = self.page.locator(".docker-contest-digest").all_inner_texts()
        return dcds

    def get_all_architecture_on_page(self, only_displayed: False):
        if only_displayed:
            architectures = self.page.locator(".d-table-row .architecture").all_inner_texts()
        else:
            architectures = self.page.locator(".architecture").all_inner_texts()
        return architectures

    def get_all_size_on_page(self, only_displayed: False):
        if only_displayed:
            sizes = self.page.locator(".d-table-row .image-size").all_inner_texts()
        else:
            sizes = self.page.locator(".image-size").all_inner_texts()
        return sizes

