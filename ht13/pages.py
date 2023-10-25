from seleniumpagefactory.Pagefactory import PageFactory


class BasePage(PageFactory):
    def __init__(self, driver, base_url):
        super().__init__()
        self.driver = driver
        self.timeout = 10  # Explicit wait
        self.base_path = base_url
        self.url = None

    def get_url(self):
        return f'{self.base_path}/{self.url}'

    def open(self):
        self.driver.get(self.get_url())


class LoginPage(BasePage):

    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.url = ''

    locators = {
        'input_username': ('ID', 'user-name'),
        'input_password': ('ID', 'password'),
        'button_login': ('NAME', 'login-button'),
        'login_credentials': ('CSS', '.login_credentials'),
        'login_password': ('XPATH', "//div[contains(@class, 'login_password')]")
    }

    def login(self, name, password):
        self.input_username.set_text(name)
        self.input_password.set_text(password)
        self.button_login.click_button()

    def get_credentials(self):
        return str(self.login_credentials.get_text()).split('\n')[1:]

    def get_password(self):
        return str(self.login_password.get_text()).split('\n')[1]


class InventoryPage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.url = 'inventory.html'
