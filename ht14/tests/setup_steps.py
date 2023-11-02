from pytest import fixture

from ht14.pages.pages import MainPage, CartPage


@fixture
def log_in(driver, existing_user):
    main_page = MainPage(driver)
    main_page.open()
    main_page.nav_bar.log_in(existing_user)


@fixture
def clear_cart(driver):
    yield
    cart_page = CartPage(driver)
    cart_page.open()
    while cart_page.wait_for_load(True):
        cart_page.get_table_data()[0].delete()
