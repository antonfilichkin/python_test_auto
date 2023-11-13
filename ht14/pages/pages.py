from os import environ
from typing import List

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

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.timeout = 10

        self.base_path = environ.get('BASE_PATH')
        self.url = ''

        self.nav_bar = NavBar(driver)
        self.locators = {}


class CommonPage(BasePage):

    def open(self):
        self.driver.get(f'{self.base_path}/{self.url}')

    def is_opened(self) -> bool:
        return self.driver.current_url.startswith(f'{self.base_path}/{self.url}')


class ByIdPage(BasePage):

    def open(self, page_id):
        self.driver.get(f'{self.base_path}/{self.url}{page_id}')

    def is_opened(self, page_id='') -> bool:
        return self.driver.current_url.startswith(f'{self.base_path}/{self.url}{page_id}')


class MainPage(CommonPage):

    def __init__(self, driver):
        super().__init__(driver)

        self.nav_bar = NavBar(driver)
        self.side_menu = SideMenu(driver)

    def get_all_cards(self) -> List[Card]:
        card_elements = self.driver.find_elements(By.CSS_SELECTOR, '#tbodyid .card')
        return [Card(self.driver, element) for element in card_elements]


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

    def add_to_cart(self, alert_timeout: int = 2):
        self.add_to_cart_button.click_button()
        wait = WebDriverWait(self.driver, alert_timeout)
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

    def wait_for_load(self, wait_for_products: bool = False, fail_if_not_found: bool = False, timeout: int = 5):
        """
        Waits for cart page to load. By default - only waits for table to be present (do not wait for products to load)
        Args:
            wait_for_products: if True - waits for at least one product to be present in table
            fail_if_not_found: if True - step would fail if wait_for_products is True, but no products were found
            timeout: seconds to wait for table/product to be present

        Returns:
            if wait_for_products is True - returns True if product was found, False - if not.
        """
        wait = WebDriverWait(self.driver, timeout)
        wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#tbodyid')))
        try:
            if wait_for_products:
                wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#tbodyid td')))
                return True
        except TimeoutException:
            if fail_if_not_found:
                raise
            else:
                LOGGER.info('Cart is empty!')
                return False

    def __table_rows__(self):
        return self.driver.find_elements(By.CSS_SELECTOR, '#tbodyid tr')

    def number_of_products_in_cart(self) -> int:
        return len(self.__table_rows__())

    def get_table_data(self) -> List[CartTableRow]:
        return [CartTableRow(self.driver, element) for element in self.__table_rows__()]

    def total(self) -> int:
        return int(self.total_summ.get_text())
