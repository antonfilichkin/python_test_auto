from logging import getLogger
from ..pages.pages import CartPage, MainPage, ProductPage
from ..pages.common import SignInModal

LOGGER = getLogger()


def test_1_login_existing_user(driver, existing_user):
    main_page = MainPage(driver)
    main_page.open()
    assert main_page.nav_bar.navbar_elements_texts() == [
        'Home', 'Contact', 'About us', 'Cart', 'Log in', 'Sign up'
    ]

    sign_in_modal = SignInModal(driver)
    main_page.nav_bar.login.click_button()
    assert sign_in_modal.username_input.is_displayed()
    assert sign_in_modal.password_input.is_displayed()

    sign_in_modal.log_in(existing_user)
    main_page.nav_bar.wait_for_logged_in()
    assert main_page.nav_bar.navbar_elements_texts() == [
        'Home', 'Contact', 'About us', 'Cart', 'Log out', f'Welcome {existing_user.name}'
    ]


def test_2_add_product_to_cart(driver, log_in, clear_cart):
    main_page = MainPage(driver)
    main_page.side_menu.select_category('Monitors')

    product_cards = main_page.get_all_cards()
    product_cards.sort(key=lambda c: c.get_price(), reverse=True)
    highest_price_product_card = product_cards[0]
    card_data = highest_price_product_card.get_data()
    highest_price_product_card.select()

    product_page = ProductPage(driver)
    assert product_page.is_opened()
    assert product_page.title.get_text() == card_data.name
    assert product_page.price.get_text() == f'${card_data.price} *includes tax'

    product_page.add_to_cart()
    product_page.nav_bar.cart.click_button()

    cart_page = CartPage(driver)
    cart_page.wait_for_load(True, True)

    assert cart_page.number_of_products_in_cart() == 1
    assert cart_page.total() == card_data.price

    product_in_cart = cart_page.get_table_data()[0]
    assert product_in_cart.get_title() == card_data.name
    assert product_in_cart.get_price() == card_data.price
