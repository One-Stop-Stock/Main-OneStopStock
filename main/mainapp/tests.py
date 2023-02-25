from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import time

class SeleniumTest(LiveServerTestCase):
    def testhomepage(self):
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

        driver.get('https://google.com')

        time.sleep(5)

        driver.quit()