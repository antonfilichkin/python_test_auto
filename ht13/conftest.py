import pytest
from selenium import webdriver


@pytest.fixture
def base_path():
    return 'https://www.saucedemo.com'


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(2)

    yield driver
    driver.quit()

