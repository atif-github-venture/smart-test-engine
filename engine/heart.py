import logging
import os
import sys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from util.common import to_snake_case
from util.webdriver import Driver


class Heart:
    errorbody = None

    def execute_step(self, i, a, d):
        self.identifier = i
        self.action = to_snake_case(a)
        self.data = d
        status = self.execute()
        if status is False or status is AttributeError:
            return status, self.errorbody
        elif status is True:
            return status
        else:
            return False, 'Unknown error'

    def execute(self):
        try:
            func = getattr(self, self.action)
            return func()
        except (AttributeError):
            self.errorbody = self.action+ ' - Invalid action, engine NOT configured!!!'
            return False

    def open_browser(self):
        d = Driver.get_driver()
        d.setUp()
        return True

    def navigate_to_url(self):
        path = (
            os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                         'temp', 'data.json'))
        from util.json import read_json_data
        data = read_json_data(path)
        url = None
        for x in data:
            url = x['key']
            if url == 'url':
                url = x['value']
                break
        driver = Driver.get_driver().driver_handle()
        driver.get(url)
        return True

    def enter_text(self):
        driver = Driver.get_driver().driver_handle()
        ele = driver.find_element_by_xpath(self.identifier)
        ele.click
        return True

    def click(self):
        return True

    def is_visible(self):
        return True

    def is_not_visible(self):
        return True

    def close_browser(self):
        Driver.tearDown()
        return True

    # def wait_for_element(self, locator, timeout=20):
    #     logging.info("# Wait for element to appear... %s" % locator)
    #     WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, locator)))
    #
    # def assert_and_click_by_xpath(self, locator):
    #     self.wait_for_element(locator)
    #     logging.info("# Click on element %s" % locator)
    #     ele = self.driver.find_element_by_xpath(locator)
    #     ele.click()
    #
    # def get_text_by_xpath(self, locator):
    #     return self.driver.find_element_by_xpath(locator).text
    #
    # def is_element_present(self, locator):
    #     try:
    #         self.driver.find_element_by_xpath(locator)
    #         logging.info("# Element '%s' is present." % locator)
    #         return True
    #     except NoSuchElementException:
    #         logging.info("# Element '%s' is not present." % locator)
    #         return False
    #
    # def assert_element_present(self, locator):
    #     logging.info("# Verifying Element is present.")
    #     assert self.is_element_present(locator), "Element '%s' should be present." % locator
    #
    # def assert_element_is_not_present(self, locator):
    #     logging.info("# Verifying Element is not present.")
    #     assert not self.is_element_present(locator), "Element '%s' should not be present." % locator
    #
    # def wait_for_element_visible(self, locator, timeout=20):
    #     logging.info("# Wait for element to appear... %s" % locator)
    #     WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
    #
    # def wait_for_element_invisible(self, locator, timeout=20):
    #     logging.info("# Wait for element to appear... %s" % locator)
    #     WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.XPATH, locator)))
    #
    # def is_element_visible(self, locator):
    #     try:
    #         ele = self.driver.find_element_by_xpath(locator)
    #         return ele.is_displayed()
    #     except NoSuchElementException:
    #         logging.info("# Element '%s' is not present." % locator)
    #     return False
    #
    # def assert_element_visibility(self, locator, is_visible=True):
    #     logging.info("# Verifying Element visibility.")
    #     assert is_visible == self.is_element_visible(locator), "Element '%s' visibility should be %s." % (
    #         locator, is_visible)
