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
        self.data = self.get_data(d)
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
            self.errorbody = self.action + ' - Invalid action, engine NOT configured!!!'
            return False

    def open_browser(self):
        d = Driver.get_driver()
        d.setUp()
        return True

    def navigate_to_url(self):
        driver = Driver.get_driver().driver_handle()
        driver.get(self.data)
        return True

    def enter_text(self):
        try:
            driver = Driver.get_driver().driver_handle()
            ele = driver.find_element_by_xpath(self.identifier)
            ele.send_keys(self.data)
            return True
        except NoSuchElementException as e:
            self.errorbody = 'NoSuchElementException' + str(e)
            return False

    def click(self):
        try:
            driver = Driver.get_driver().driver_handle()
            ele = driver.find_element_by_xpath(self.identifier)
            ele.click()
            return True
        except NoSuchElementException as e:
            self.errorbody = 'NoSuchElementException' + str(e)
            return False

    def is_visible(self):
        try:
            driver = Driver.get_driver().driver_handle()
            ele = driver.find_element_by_xpath(self.identifier)
            return ele.is_displayed()
        except NoSuchElementException as e:
            self.errorbody = 'NoSuchElementException' + str(e)
            return False

    def is_not_visible(self):
        try:
            driver = Driver.get_driver().driver_handle()
            ele = driver.find_element_by_xpath(self.identifier)
            return not (ele.is_displayed())
        except NoSuchElementException as e:
            self.errorbody = 'NoSuchElementException' + str(e)
            return False

    def close_browser(self):
        self.quit_driver()
        return True

    def wait_for_element(self, timeout=20):
        try:
            driver = Driver.get_driver().driver_handle()
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, self.identifier)))
            return True
        except Exception as e:
            self.errorbody = 'Exception' + str(e)
            return False

    def wait_for_visibility(self, timeout=20):
        try:
            driver = Driver.get_driver().driver_handle()
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, self.identifier)))
            return True
        except Exception as e:
            self.errorbody = 'Exception' + str(e)
            return False

    def wait_for_invisibility(self, timeout=20):
        try:
            driver = Driver.get_driver().driver_handle()
            WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((By.XPATH, self.identifier)))
            return False
        except Exception as e:
            self.errorbody = 'Exception' + str(e)
            return True

    def get_text(self):
        try:
            driver = Driver.get_driver().driver_handle()
            ele = driver.find_element_by_xpath(self.identifier)
            return ele.text
        except NoSuchElementException as e:
            self.errorbody = 'NoSuchElementException' + str(e)
            return False

    def is_present(self):
        try:
            driver = Driver.get_driver().driver_handle()
            driver.find_element_by_xpath(self.identifier)
            return True
        except NoSuchElementException as e:
            self.errorbody = 'NoSuchElementException' + str(e)
            return False

    def is_not_present(self):
        try:
            driver = Driver.get_driver().driver_handle()
            driver.find_element_by_xpath(self.identifier)
            return False
        except NoSuchElementException as e:
            self.errorbody = 'NoSuchElementException' + str(e)
            return True

    def get_data(self, search):
        path = (
            os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                         'temp', 'data.json'))
        from util.json import read_json_data
        data = read_json_data(path)
        valuetoreturn = None
        for x in data:
            valuetoreturn = x['key']
            if valuetoreturn == search:
                valuetoreturn = x['value']
                break
        return valuetoreturn

    def quit_driver(self):
        Driver.get_driver().driver_handle().quit()
