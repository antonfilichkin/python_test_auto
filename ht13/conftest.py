import pytest
from selenium import webdriver


@pytest.fixture
def base_path():
    return 'https://www.saucedemo.com'


@pytest.fixture
def driver():
    driver = chrome_driver()

    yield driver
    driver.quit()


def chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options)
    driver.implicitly_wait(2)

    return driver
