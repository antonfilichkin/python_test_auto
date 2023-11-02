from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import re


class NavBar(PageFactory):

    __navbar_menu_items_css__ = (f'#navbarExample li:nth-child({index})' for index in range(1, 9))
    __names__ = ('home', 'contact', 'about_us', 'cart', 'login', 'logout', 'signup', 'welcome_user')
    locators = {key: ('CSS', locator) for key, locator in zip(__names__, __navbar_menu_items_css__)}

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def navbar_elements_texts(self):
        raw_texts = [element.text for element in self.driver.find_elements(By.CSS_SELECTOR, '#navbarExample li')]
        return [re.sub(r'\n\(.*?\)', '', element) for element in raw_texts if element]

    def log_in(self, user):
        self.login.click()
        SignInModal(self.driver).log_in(user)
        self.wait_for_logged_in()

    def log_out(self):
        self.logout.click()
        self.wait_for_logged_out()

    def wait_for_logged_in(self):
        self.__wait_for_fifth_nav_menu_item_to_be__('Log out')

    def wait_for_logged_out(self):
        self.__wait_for_fifth_nav_menu_item_to_be__('Log in')

    def __wait_for_fifth_nav_menu_item_to_be__(self, expected):
        wait = WebDriverWait(self.driver, 2)
        wait.until(
            lambda driver: self.navbar_elements_texts()[4] == expected
        )


class SideMenu(PageFactory):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

        menu_items_css = (f'#contcont a.list-group-item:nth-child({index})' for index in range(2, 5))
        names = ('Phones', 'Laptops', 'Monitors')
        self.locators = {key: ('CSS', locator) for key, locator in zip(names, menu_items_css)}

    def categories_texts(self):
        return [element.text for element in self.driver.find_elements(By.CSS_SELECTOR, self.__menu_items_css__)]

    def select_category(self, category):
        first_card = self.driver.find_element(By.CSS_SELECTOR,  '#tbodyid div.card')
        self.__getattr__(category).click_button()
        wait = WebDriverWait(self.driver, 2)
        wait.until(ec.staleness_of(first_card))


class Modal(PageFactory):

    locators = {}

    def __init__(self, driver, modal_id):
        super().__init__()
        self.driver = driver
        self.__modal_id__ = modal_id
        self.locators['modal'] = 'ID', f'#{modal_id}'
        self.locators['close_button'] = 'CSS', f'#{modal_id} button[data-dismiss="modal"]'

    def is_shown(self):
        self.modal.is_displayed()

    def close(self):
        self.close_button.click_button()
        self.wait_for_close()

    def wait_for_close(self):
        wait = WebDriverWait(self.driver, 2)
        wait.until(ec.invisibility_of_element_located((By.ID, self.__modal_id__)))


class SignInModal(Modal):

    def __init__(self, driver):
        super().__init__(driver, 'logInModal')
        self.locators = self.locators | {
            'username_input': ('ID', 'loginusername'),
            'password_input': ('ID', 'loginpassword'),
            'login_button': ('CSS', 'button[onclick="logIn()"]'),
        }

    def log_in(self, user):
        self.username_input.send_keys(user.name)
        self.password_input.send_keys(user.password)
        self.login_button.click_button()
        self.wait_for_close()
