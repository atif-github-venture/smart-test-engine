import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Driver:
    driver = None

    def setUp(self, test_name, type, ip):
        print('driver setup...')
        import time
        time.sleep(5)
        try:
            path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                                'resources')
            if type == 'local':
                dc = self.create_desired_capabilities(test_name)
                self.driver = webdriver.Chrome(executable_path=path + '/chromedriver', desired_capabilities=dc)
            elif type == 'sauce':
                dc = self.create_desired_capabilities(test_name)
                self.driver = webdriver.Remote(
                    command_executor="https://fatebamboo:9099ed6e-b6ab-42d0-a2d1-76fe26985c74@ondemand.saucelabs.com:443/wd/hub",
                    desired_capabilities=dc)
            elif type == 'seleniumgrid':
                self.driver = webdriver.Remote(
                    command_executor='http://localhost:4444/wd/hub',
                    desired_capabilities=DesiredCapabilities.CHROME)
            elif type == 'digitalocean':
                print('digital ocean block...')
                print('ip: '+ip)
                if ip is None:
                    raise Exception('IP is empty and not set, somewthing wrong in the cloud image creation :(:(:(')
                print('lets connect to remote...')
                self.driver = webdriver.Remote(
                    command_executor='http://'+ip+':4444/wd/hub',
                    desired_capabilities=DesiredCapabilities.CHROME)
                print('connected to remote...')
            else:
                return None
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            return self.driver
        except WebDriverException as e:
            print('Failure in driver setup()...')
            print(str(e))
            return None

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
