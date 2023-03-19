from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

def home_view(request, *args, **kwargs):
    input = request.POST.get('store-item')
    print(input)
    if not input:
        return render(request, "home.html", {'input': input})
    
    content = getResult(input)
    return render(request, "home.html", {'input': content})

def about_view(request, *args, **kwargs):
    return render(request, "about.html", {})

def getResult(input):
    #Change driver and driver location
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    walmartLink = "https://www.target.com/s?searchTerm="
    itemSearch = input
    link = walmartLink + itemSearch
    driver.get(link)
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    content = list()
    k = {}

    """ #Walmart Test
    #finding all the items on the page
    try:
        item = soup.find_all("span", {"class" : "w_V_DM"})
    except:
        item = None
    
    #Only get the first 4 items
    for i in range (0,4):
        try:
            k["Item{}".format(i + 1)] = item[i].find("span", {"data-automation-id": "product-title"}).text.replace("\n","")
        except:
            k["Item{}".format(i + 1)] = None
    content.append(k)
    k = {}
    """

    '''
    #Only get the first 4 items
    for i in range (0,4):
        try:
            k["Item{}".format(i + 1)] = item[i].find("span", {"data-automation-id": "product-title"}).text.replace("\n","")
        except:
            k["Item{}".format(i + 1)] = None
    content.append(k)
    k = {}
    '''
    
    #Target Testing
    try:
        item = soup.find_all("div", {"class": "Truncate-sc-10p6c43-0 flAIvs"})
    except:
        item = None
    
    #finds all image links on the website and storing it into a list
    links = list()
    images = soup.find_all('img')
    for img in images:
        if img.has_attr('src'):
            links.append(img['src'])

    #Slicing up 'duplicate links'
    temp = links[2:10]
    newLinks = temp[::2]
    
    #the list 'newLinks' contains 4 links
    #return (newLinks)
    

    for i in range(0, 4):
        try:
            k["Item{}".format(i + 1)] = item[i].find("a", {"data-test": "product-title"}).text.replace("\n", "")
        except:
            k["Item{}".format(i + 1)] = None
        content.append(k)
        k = {}


    return (content)

""" def tristen_a3p3(request, *args, **kwargs):
    return render(request, "tristena3p3.html", {})

def ryleya3p3(request, *args, **kwargs):
    return render(request, "ryleya3p3.html", {})	

def ryana3p3(request, *args, **kwargs):
    return render(request, "ryana3p3.html", {}) """



