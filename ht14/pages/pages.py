from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.support.wait import WebDriverWait
from .common import NavBar, SignInModal


class BasePage(PageFactory):

    def __init__(self, driver, base_url):
        super().__init__()
        self.driver = driver
        self.timeout = 10  # Explicit wait
        self.base_path = base_url
        self.nav_bar = NavBar(driver)
        self.url = None

    def get_url(self):
        return f'{self.base_path}/{self.url}'

    def open(self):
        self.driver.get(self.get_url())
        return self

    def login(self, user):
        self.nav_bar.login.click()
        SignInModal(self.driver).login(user)
        self.wait_for_logged_in()
        return self

    def logout(self, user):
        self.nav_bar.login.click()
        SignInModal(self.driver).login(user)
        self.wait_for_logged_out()
        return self

    def wait_for_logged_in(self):
        self.__wait_for_fifth_nav_menu_item_to_be__('Log out')

    def wait_for_logged_out(self):
        self.__wait_for_fifth_nav_menu_item_to_be__('Log in')

    def __wait_for_fifth_nav_menu_item_to_be__(self, expected):
        wait = WebDriverWait(self.driver, 2)
        wait.until(
            lambda driver: self.nav_bar.navbar_elements_texts()[4] == expected
        )


class MainPage(BasePage):

    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.url = ''
