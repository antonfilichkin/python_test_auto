from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


class ScreenshotListener:
    ROBOT_LISTENER_API_VERSION = 2

    TRIGGER_TAG = 'Screenshot'

    def end_keyword(self, name, attributes):
        if self.TRIGGER_TAG in attributes['tags']:
            logger.info('Attaching Screenshot As Requested Via Tag')
            selenium = BuiltIn().get_library_instance('SeleniumLibrary')
            selenium.capture_page_screenshot('EMBED')
