from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

def home_view(request, *args, **kwargs):
    input = request.POST.get('store-item')
    print(input)
    if not input:
        return render(request, "home.html", {'input': input})
    
    content = getResult(input)
    images = getImage()
    
    return render(request, "home.html", {'input':content , 'images':images})

def about_view(request, *args, **kwargs):
    return render(request, "about.html", {})

def getResult(input):
    global imageList
    #Change driver and driver location

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    targetLink = "https://www.target.com/s?searchTerm="

    itemSearch = input

    #targetLink = "https://www.target.com/s?searchTerm="
    # link = targetLink + itemSearch

    dollarLink = "https://www.dollartree.com/searchresults?Ntt="
    link  = dollarLink + itemSearch

    driver.get(link)
    time.sleep(8)
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
    
    
    #Target Testing
    try:
        item = soup.find_all("div", {"class": "Truncate-sc-10p6c43-0 flAIvs"})
    except:
        item = None
    
    """
    OUTDATED - KEEPING THIS HERE JUST IN CASE SOMETHING BREAKS

    #finds all image links on the website and storing it into a list
    links = list()
    images = soup.find_all('img')
    for img in images:
        if img.has_attr('src'):
            links.append(img['src'])

    print(links)
    
    #Slicing up 'duplicate links'
    temp = links[3:10]
    newLinks = temp[::2]
    """"
    """

    #New version of image retrieval 
    #Tells soup to find all of our images wthin a certain section (ie the product section, ignoring ads or other misc)
    links = list()
    for images in soup.find_all("picture", {"data-test" : "@web/ProductCard/ProductCardImage/primary"}):
        for img in images.find_all("img"):
            links.append(img['src'])

    temp = links[:4] #Condense down the amount of links into 4
    imageList = temp #shipping it off
    

    for i in range(0, 4):
        try:
            k["Item{}".format(i + 1)] = item[i].find("a", {"data-test": "product-title"}).text.replace("\n", "")
        except:
            k["Item{}".format(i + 1)] = None
        content.append(k)
        k = {}
    '''


    #Dollar Tree Testing
    items = list()

    try:
        entry = soup.find_all("span", {"data-bind": "html: displayName"})
    except:
        entry = None

    count = 1
    for i in range(0, 8, 2):
        try:
            k["Item {}".format(count)] = entry[i].text
        except:
            k["Item{}".format(i + 1)] = None
        items.append(k)
        k = {}
        count = count + 1

    links = list()
    for images in soup.find_all("img", {"class": "bg-product-image"}):
        links.append(images['src'])

    tempString = "https://www.dollartree.com"
    temp = links[:4]
    newLinks = [tempString + s for s in temp]

    imageList = newLinks

    return (items)

def getImage():
    global imageList
    return imageList


""" def tristen_a3p3(request, *args, **kwargs):
    return render(request, "tristena3p3.html", {})

def ryleya3p3(request, *args, **kwargs):
    return render(request, "ryleya3p3.html", {})	

def ryana3p3(request, *args, **kwargs):
    return render(request, "ryana3p3.html", {}) """



