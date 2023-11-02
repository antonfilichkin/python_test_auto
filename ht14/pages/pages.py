from os import environ

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from seleniumpagefactory.Pagefactory import PageFactory
from logging import getLogger

from .common import NavBar, SideMenu
from .elements import Card, CartTableRow

LOGGER = getLogger()


class BasePage(PageFactory):

    locators = {}

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.timeout = 10
        self.base_path = environ.get('BASE_PATH')
        self.nav_bar = NavBar(driver)
        self.url = ''


class CommonPage(BasePage):

    def open(self):
        self.driver.get(f'{self.base_path}/{self.url}')

    def is_opened(self):
        return self.driver.current_url.startswith(f'{self.base_path}/{self.url}')


class ByIdPage(BasePage):

    def open(self, product_id):
        self.driver.get(f'{self.base_path}/{self.url}{product_id}')

    def is_opened(self, product_id=''):
        return self.driver.current_url.startswith(f'{self.base_path}/{self.url}{product_id}')


class MainPage(CommonPage):

    def __init__(self, driver):
        super().__init__(driver)
        self.nav_bar = NavBar(driver)
        self.side_menu = SideMenu(driver)

    def get_all_cards(self):
        cards = []
        for element in self.driver.find_elements(By.CSS_SELECTOR, '#tbodyid .card'):
            cards.append(Card(self.driver, element))
        return cards


class ProductPage(ByIdPage):

    def __init__(self, driver):
        super().__init__(driver)
        self.url = 'prod.html?idp_='
        self.locators = self.locators | {
            'title': ('CSS', '#tbodyid .name'),
            'price': ('CSS', '#tbodyid .price-container'),
            'description': ('CSS', '#tbodyid .description'),
            'add_to_cart_button': ('CSS', '#tbodyid a'),
        }

    def add_to_cart(self):
        self.add_to_cart_button.click_button()
        wait = WebDriverWait(self.driver, 2)
        wait.until(ec.alert_is_present())
        self.driver.switch_to.alert.dismiss()


class CartPage(CommonPage):

    def __init__(self, driver):
        super().__init__(driver)
        self.url = 'cart.html'
        self.locators = self.locators | {
            'title': ('CSS', '#tbodyid .name'),
            'price': ('CSS', '#tbodyid .price-container'),
            'description': ('CSS', '#tbodyid .description'),
            'add_to_cart_button': ('CSS', '#tbodyid a'),
            'total_summ': ('ID', 'totalp'),
        }

    def wait_for_load(self, wait_for_products: bool = False, fail_if_products_not_found: bool = False):
        wait = WebDriverWait(self.driver, 5)
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#tbodyid')))
        try:
            if wait_for_products:
                wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#tbodyid td')))
                return 1
        except TimeoutException:
            if fail_if_products_not_found:
                raise
            else:
                LOGGER.info('Cart is empty!')
                return 0

    def table_rows(self):
        return self.driver.find_elements(By.CSS_SELECTOR, '#tbodyid tr')

    def number_of_products_in_cart(self):
        return len(self.table_rows())

    def get_table_data(self, ):
        table_data = []
        for element in self.table_rows():
            table_data.append(CartTableRow(self.driver, element))
        return table_data

    def total(self):
        return int(self.total_summ.get_text())
