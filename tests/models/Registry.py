from app import Config

config = Config()


class RegistryPage:
    def __init__(self, page):
        self.page = page
        self.nav_tab = page.locator("#nav-tab")
        self.nav_tabs = page.locator("#nav-tab > li")
        self.nav_tab_buttons = page.locator(".nav-tabs > .nav-item > button")
        self.registry_tables = page.locator("#registry-tables")
        self.show_images_without_tags_checkbox = page.locator("#check-show-without-tags")
        self.filter_by_name_input = page.locator("#repository-search")
        self.all_repository_names_of_active_pane = (
            page.locator(f".active > table > tbody > .repository-row > td > .repository-name"))
        self.displayed_repository_names_of_active_pane = (
            page.locator(f".active > table > tbody > .repository-row.d-table-row > td > .repository-name"))
        self.displayed_repository_counted_tags_of_active_pane = (
            page.locator(f".active > table > tbody > .repository-row.d-table-row > td.count-tags"))
        self.registry_name = page.locator(".nav-link.active").all_inner_texts()

    def navigate(self):
        self.page.goto(url=f"{config.APP_URL}/registry")

    def navigate_to_repository(self, child):
        self.displayed_repository_names_of_active_pane.all()[child].click()

    # def get_repository_names_of_active_pane(self):
    #     rows = self.page.locator(f".active > table > tbody > .repository-row > td > .repository-name")
    #     return rows
    #
    # def get_displayed_repository_names_of_active_pane(self):
    #     rows = self.page.locator(f".active > table > tbody > .repository-row.d-table-row > td > .repository-name")
    #     return rows

