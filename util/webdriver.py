import logging
import sys, os

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class Driver():
    def setUp(self):
        # self.ffprofile = self.create_ffprofile()
        # self.driver = webdriver.Firefox(self.ffprofile)
        try:
            path = os.path.join(os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)),
                                     'resources')
            self.driver = webdriver.Chrome(executable_path=path+'/chromedriver')
            self.driver.maximize_window()
            self.driver.implicitly_wait(5)
            self.driver.get("http://google.com/")
        except WebDriverException as e:
            print(str(e))
            return None
        return self.driver

    def tearDown(self):
        if sys.exc_info()[0]:
            self.driver.save_screenshot("./../screenshots.png")
        if self.driver is not None:
            self.driver.quit()

    def create_ffprofile(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2)  # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', os.getcwd())
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk',
                               'text/csv,application/octet-stream,application/pdf,application/vnd.ms-excel')
        profile.set_preference("pdfjs.disabled", True)

        return profile
