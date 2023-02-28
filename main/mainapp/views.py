from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time

def home_view(request, *args, **kwargs):
    input = request.POST.get('store-item')
    print(input)
    if not input:
        return render(request, "home.html", {'input': input})
    else:
        content = getResult(input)
        return render(request, "home.html", {'input': input})

def tristen_a3p3(request, *args, **kwargs):
    return render(request, "tristena3p3.html", {})

def ryleya3p3(request, *args, **kwargs):
    return render(request, "ryleya3p3.html", {})	

def ryana3p3(request, *args, **kwargs):
    return render(request, "ryana3p3.html", {})

def getResult(input):
    #Change driver and driver location
    driver = webdriver.Chrome("C://Users/cubix/Downloads/chromedriver.exe")
    walmartLink = "https://www.walmart.com/search?q="
    itemSearch = input
    url = walmartLink + itemSearch
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    content = list()
    k = {}

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

    return (content)



