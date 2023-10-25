from selenium.webdriver.common.by import By
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
        return self


class LoginPage(BasePage):

    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.url = ''

    locators = {
        'username_input': ('ID', 'user-name'),
        'password_input': ('ID', 'password'),
        'login_button': ('NAME', 'login-button'),

        'login_credentials': ('CSS', '.login_credentials'),
        'login_password': ('XPATH', "//div[contains(@class, 'login_password')]"),

        'login_error_message': ('CSS', '.error-message-container h3'),
        'login_error_message_button': ('CSS', '.error-message-container button')
    }

    def login(self, name, password):
        self.username_input.set_text(name)
        self.password_input.set_text(password)
        self.login_button.click_button()

    def get_credentials(self):
        return str(self.login_credentials.get_text()).split('\n')[1:]

    def get_password(self):
        return str(self.login_password.get_text()).split('\n')[1]

    def is_login_error_shown(self):
        return len(self.driver.find_elements(By.CSS_SELECTOR, '.error-message-container > h3')) > 0

    def get_login_error_text(self):
        return self.login_error_message.get_text()

    def close_login_error(self):
        return self.login_error_message_button.click_button()


class InventoryPage(BasePage):
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.url = 'inventory.html'
