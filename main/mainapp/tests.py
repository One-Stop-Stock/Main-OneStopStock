from django.test import LiveServerTestCase
from selenium import webdriver

class SeleniumTest(LiveServerTestCase):
    def testhomepage(self):
        driver = webdriver.Edge()

        driver.get('https://google.com')