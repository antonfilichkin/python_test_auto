from pytest import fixture

from ..pages.pages import CartPage, MainPage


@fixture
def log_out(driver):
    yield
    main_page = MainPage(driver)
    main_page.open()
    main_page.nav_bar.log_out()


@fixture
def clear_cart(driver):
    yield
    cart_page = CartPage(driver)
    cart_page.open()
    while cart_page.wait_for_load(True):
        cart_page.get_table_data()[0].delete()
