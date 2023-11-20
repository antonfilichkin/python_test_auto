from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import timestr_to_secs


class SeleniumCustom:

    def wait_until_element_is_stale(self, web_element, timeout, poll_interval):
        selenium = BuiltIn().get_library_instance('SeleniumLibrary')
        wait = WebDriverWait(selenium.driver, timestr_to_secs(timeout), timestr_to_secs(poll_interval))
        wait.until(ec.staleness_of(web_element))
