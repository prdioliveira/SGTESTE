from django.contrib.staticfiles.testing import StaticLiveServerTestCase, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class FunctionalTest(StaticLiveServerTestCase):
    """
    Launches a live Django server in the background on setup, and
    shuts it down on teardown. This allows the use of automated test
    clients other than the Django dummy client such as, for example,
    the Selenium client, to execute a series of functional tests
    inside a browser and simulate a real user’s actions.

    We’ll use the StaticLiveServerTestCase subclass with serves static
    files during the execution of tests similar to what we get at
    development time with DEBUG=True, i.e. without having to collect
    them using collectstatic.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = WebDriver()
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()