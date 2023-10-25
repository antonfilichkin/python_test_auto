from pages import LoginPage, InventoryPage


def test_login_first_user_and_get_current_url(driver, base_path):
    login_page = LoginPage(driver, base_path)
    inventory_page = InventoryPage(driver, base_path)

    login_page.open()

    standard_user = login_page.get_credentials()[0]
    user_pass = login_page.get_password()

    login_page.login(standard_user, user_pass)

    assert driver.current_url == inventory_page.get_url()
