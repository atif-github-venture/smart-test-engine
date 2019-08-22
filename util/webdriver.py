import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Driver():
    driver = None
    def setUp(self, test_name, type):
        dc = self.create_desired_capabilities(test_name)
        try:
            path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                                'resources')
            if type == 'local':
                self.driver = webdriver.Chrome(executable_path=path + '/chromedriver', desired_capabilities=dc)
            elif type == 'sauce':
                self.driver = webdriver.Remote(command_executor="https://fatebamboo:9099ed6e-b6ab-42d0-a2d1-76fe26985c74@ondemand.saucelabs.com:443/wd/hub", desired_capabilities=dc)
            else:
                return None
            self.driver.maximize_window()
            self.driver.implicitly_wait(5)
            return self.driver
        except WebDriverException as e:
            print(str(e))

    def create_desired_capabilities(self, test_name):
        path = (
            os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                         'temp', 'config.json'))
        from util.json import read_json_data
        conf = read_json_data(path)
        dc = DesiredCapabilities.CHROME
        dc.update(conf[0]['properties'])
        dc.update({'name': test_name})
        return dc
