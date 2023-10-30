from logging import getLogger
from ..pages.pages import MainPage
from ..pages.common import SignInModal

LOGGER = getLogger()

expected_navmenu_guest = ['Home', 'Contact', 'About us', 'Cart', 'Log in', 'Sign up']


def test_1_login_existing_user(driver, base_path, existing_user):
    expected_navmenu_logged = ['Home', 'Contact', 'About us', 'Cart', 'Log out', f'Welcome {existing_user.name}']

    main_page = MainPage(driver, base_path)
    sign_in_modal = SignInModal(driver)

    main_page.open()
    assert main_page.nav_bar.navbar_elements_texts() == expected_navmenu_guest

    main_page.nav_bar.login.click_button()
    assert sign_in_modal.username_input.is_displayed()
    assert sign_in_modal.password_input.is_displayed()

    sign_in_modal.login(existing_user)
    main_page.wait_for_logged_in()
    assert main_page.nav_bar.navbar_elements_texts() == expected_navmenu_logged
