import json
import logging
import sys, os

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Driver():
    __instance = None
    driver = None

    @staticmethod
    def get_driver():
        if Driver.__instance is None:
            Driver()
        return Driver.__instance

    def __init__(self):
        Driver.__instance = self

    def driver_handle(self):
        return self.driver

    def setUp(self):
        dc = self.create_desired_capabilities()
        try:
            path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                                'resources')
            self.driver = webdriver.Chrome(executable_path=path + '/chromedriver', desired_capabilities=dc)
            self.driver.maximize_window()
            self.driver.implicitly_wait(5)
        except WebDriverException as e:
            print(str(e))

    def tearDown(self):
        if sys.exc_info()[0]:
            self.driver.save_screenshot("./../screenshots.png")
        if self.driver is not None:
            self.driver.quit()

    def create_desired_capabilities(self):
        path = (
            os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                         'temp', 'config.json'))
        from util.json import read_json_data
        conf = read_json_data(path)
        dc = DesiredCapabilities.CHROME
        dc.update(conf[0]['properties'])
