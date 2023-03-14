import unittest
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

#testing webdriver manager
class WebDriverManagerTest(unittest.TestCase):
    def testGetResult(self):
        #Change driver and driver location
        #Webdriver notation found here: https://pypi.org/project/webdriver-manager/
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        walmartLink = "https://www.target.com/s?searchTerm="
        itemSearch = "coke"
        link = walmartLink + itemSearch
        driver.get(link)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.close()

        content = list()
        k = {}

        try:
            item = soup.find_all("div", {"class": "Truncate-sc-10p6c43-0 flAIvs"})
        except:
            item = None

        for i in range(0, 4):
            try:
                k["Item{}".format(i + 1)] = item[i].find("a", {"data-test": "product-title"}).text.replace("\n", "")
            except:
                k["Item{}".format(i + 1)] = None
            content.append(k)
            k = {}
            
            return (content)
