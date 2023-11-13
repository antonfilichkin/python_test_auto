from pytest import fixture

from ..pages.pages import MainPage
from ..test_data.users import existing_user


@fixture
def log_in(driver, existing_user):
    main_page = MainPage(driver)
    main_page.open()
    main_page.nav_bar.log_in(existing_user)
