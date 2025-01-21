from app import Config

config = Config()


class NavigationPage:
    def __init__(self, page):
        self.page = page
        self.home_button = page.locator("#home")
        self.registry_explorer_button = page.locator("#registry-explorer")
        self.english_button = page.locator("#lang-en")
        self.polish_button = page.locator("#lang-pl")
        self.light_theme_button = page.locator("#light-theme")
        self.dark_theme_button = page.locator("#dark-theme")
        self.logout_button = page.locator("#logout")
        self.html_tag = page.locator("html")

    def navigate(self):
        self.page.goto(url=config.APP_URL)

