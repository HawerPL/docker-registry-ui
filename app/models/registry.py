
class Registry:
    def __init__(self, name, login, password, url, is_deletable):
        self.name = name
        self.login = login
        self.password = password
        self.url = url
        self.repositories = []
        self.isAvailable = False
        self.isDeletable = is_deletable

    def __str__(self):
        return f"Registry(name={self.name}, login={self.login}, password=****, url={self.url})"


