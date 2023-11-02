from seleniumpagefactory.Pagefactory import PageFactory
from selenium.webdriver.common.by import By


class Card(PageFactory):

    def __init__(self, driver, web_element):
        super().__init__()
        self.driver = driver
        self.web_element = web_element

    def get_data(self):
        return type('Card_repr', (), {
            'name': self.get_name(),
            'price': self.get_price(),
            'article': self.get_article(),
        })

    def get_name(self):
        return self.web_element.find_element( By.CSS_SELECTOR, 'h4').get_text()

    def get_price(self):
        return int(self.web_element.find_element(By.CSS_SELECTOR, 'h5').get_text()[1:])

    def get_article(self):
        return self.web_element.find_element(By.CSS_SELECTOR, 'p').get_text()

    def select(self):
        return self.web_element.find_element(By.CSS_SELECTOR, 'a').click()


class CartTableRow(PageFactory):

    def __init__(self, driver, web_element):
        super().__init__()
        self.driver = driver
        self.web_element = web_element

    def get_data(self):
        return type('Table_row_repr', (), {
            'img_src': self.get_img_src(),
            'title': self.get_title(),
            'price': self.get_price(),
        })

    def get_img_src(self):
        return self.web_element.find_element(By.CSS_SELECTOR, 'td:nth-child(1) img').get_attribute('src')

    def get_title(self):
        return self.web_element.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').get_text()

    def get_price(self):
        return int(self.web_element.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').get_text())

    def delete(self):
        return self.web_element.find_element(By.CSS_SELECTOR, 'td:nth-child(4) a').click()
