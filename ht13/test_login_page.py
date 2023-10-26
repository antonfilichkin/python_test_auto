from pages import LoginPage, InventoryPage


def test_login_standard_user_and_get_current_url(driver, base_path):
    login_page = LoginPage(driver, base_path)
    inventory_page = InventoryPage(driver, base_path)

    login_page.open()

    standard_user = login_page.get_credentials()[0]
    user_pass = login_page.get_password()

    login_page.login(standard_user, user_pass)

    assert driver.current_url == inventory_page.get_url()


def test_login_locked_out_user(driver, base_path):
    login_page = LoginPage(driver, base_path).open()

    locked_out_user = login_page.get_credentials()[1]
    user_pass = login_page.get_password()

    assert not login_page.is_login_error_shown()
    login_page.login(locked_out_user, user_pass)
    assert login_page.is_login_error_shown()
    assert login_page.get_login_error_text() == 'Epic sadface: Sorry, this user has been locked out.'
    login_page.close_login_error()
    assert not login_page.is_login_error_shown()
