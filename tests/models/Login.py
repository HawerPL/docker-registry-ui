from app import Config

config = Config()


class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.registry_input = page.locator("#registry")
        self.submit_input = page.locator("#loginSubmit")

    def navigate(self):
        self.page.goto(url=config.APP_URL)

    def login(self, username, password, registry):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.registry_input.select_option(registry)
        self.submit_input.click()

