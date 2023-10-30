import os

from pytest import fixture, hookimpl
from selenium import webdriver
from logging import getLogger
from datetime import datetime

from ..test_data.users import *

LOGGER = getLogger()


@fixture
def base_path():
    return 'https://www.demoblaze.com'


@fixture(scope='session')
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


@hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    if result.failed:
        if 'driver' in item.fixturenames:
            driver = item.funcargs['driver']
        else:
            LOGGER.warning('WebDriver was not found. Skipping screenshot generation!')
            return

        file_name = datetime.now().strftime(f'{item.keywords.node.originalname}_%Y%m%d_%H-%M-%S')
        folder_name = 'screenshots'
        create_screenshots_folder(folder_name)
        capture_path = f'./{folder_name}/{file_name}.png'
        driver.save_screenshot(capture_path)


def create_screenshots_folder(folder_name):
    if not os.path.exists(f'./{folder_name}'):
        os.makedirs(f'./{folder_name}')
