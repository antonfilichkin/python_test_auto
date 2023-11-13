from dataclasses import dataclass

from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By


@dataclass
class CardRepr:
    name: str
    price: int
    article: str


class Card(PageFactory):

    def __init__(self, driver, root_web_element):
        super().__init__()
        self.driver = driver
        self.web_element = root_web_element

    def get_data(self) -> CardRepr:
        return CardRepr(self.get_name(), self.get_price(), self.get_article())

    def get_name(self) -> str:
        return self.web_element.find_element(By.CSS_SELECTOR, 'h4').get_text()

    def get_price(self) -> int:
        return int(self.web_element.find_element(By.CSS_SELECTOR, 'h5').get_text()[1:])

    def get_article(self) -> str:
        return self.web_element.find_element(By.CSS_SELECTOR, 'p').get_text()

    def select(self):
        return self.web_element.find_element(By.CSS_SELECTOR, 'a').click()


@dataclass
class TableRowRepr:
    img_src: str
    title: str
    price: int


class CartTableRow(PageFactory):

    def __init__(self, driver, root_web_element):
        super().__init__()
        self.driver = driver
        self.web_element = root_web_element

    def get_data(self) -> TableRowRepr:
        return TableRowRepr(self.get_img_src(), self.get_title(), self.get_price())

    def get_img_src(self) -> str:
        return self.web_element.find_element(By.CSS_SELECTOR, 'td:nth-child(1) img').get_attribute('src')

    def get_title(self) -> str:
        return self.web_element.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').get_text()

    def get_price(self) -> int:
        return int(self.web_element.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').get_text())

    def delete(self):
        return self.web_element.find_element(By.CSS_SELECTOR, 'td:nth-child(4) a').click()
