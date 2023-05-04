from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import re

def home_view(request, *args, **kwargs):
    input = request.POST.get('store-item')
    zipcode = request.POST.get('location-zip')
    print(input)
    if not input:
        return render(request, "home.html", {'input': input})
    
    #content = targetStore(input, zipcode)
    #images = getImage()
    store1 = targetStore(input, zipcode)
    store2 = dollarGeneral(input, zipcode)
    store3 = walgreenStore(input, zipcode)
    images1 = imageList1
    images2 = imageList2
    images3 = imageList3
    
    return render(request, "home.html", {'store1':store1, 'images1':imageList1,
                                         'store2':store2, 'images2':imageList2,
                                         'store3':store3, 'images3':imageList3,})

def about_view(request, *args, **kwargs):
    return render(request, "about.html", {})

def targetStore(input, zipcode):
    global imageList1

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    url = "https://www.target.com/s?searchTerm=" + input

    driver.get(url)
    driver.maximize_window()

    time.sleep(15)
    driver.execute_script("window.scrollTo(0,600);")
    time.sleep(15)

    #Location Based Searching
    """
    element = driver.find_element(By.ID,"web-store-id-msg-btn")
    element.click()
    time.sleep(4)
    element = driver.find_element(By.ID,"zip-or-city-state")
    element.click()
    element.send_keys(zipcode)
    xpath = "/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/div[2]/button"
    element = driver.find_element(By.XPATH,xpath)
    element.click()
    time.sleep(8)
    #xpath2 = "/html/body/div[5]/div/div/div[2]/div[2]/fieldset/div[3]/div/div[1]/label/div/div/h4"
    #element = driver.find_element(By.XPATH,xpath2)
    #element.click()
    #time.sleep(4)
    xpath3 = "/html/body/div[5]/div/div/div[3]/button"
    element = driver.find_element(By.XPATH,xpath3)
    element.click()
    time.sleep(6)
    driver.execute_script("window.scrollTo(0,600);")
    time.sleep(10)
    """

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    k = {}
    items = list()

    #Searching for all items
    try:
        entry = soup.find_all("div", {"class": "Truncate-sc-10p6c43-0 flAIvs"})
    except:
        entry = None

    #Limited items to 4
    for i in range(0, 4):
        try:
            k["Title{}".format(i + 1)] = entry[i].find("a", {"data-test": "product-title"}).text.replace("\n",
                                                                                                                    "")
        except:
            k["Title{}".format(i + 1)] = None
        items.append(k)
        k = {}

    #Searches for all item images
    links = list()
    for images in soup.find_all("picture", {"data-test" : "@web/ProductCard/ProductCardImage/primary"}):
        for img in images.find_all("img"):
            links.append(img['src'])

    #Limit the images to the first 4 products and store it inside a global variabl
    imageList1 = links[:4]

    #return the items
    return items

def dollarGeneral(input, zipcode):
    global imageList2

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    url = "https://www.dollargeneral.com/product-search.html?q="
    inStock = "&inStock=true"
    fullUrl = url + input + inStock
    driver.get(fullUrl)
    time.sleep(15)

    """
    xpath = "/html/body/div[1]/div/div[1]/div/div/header/div/div[2]/div[1]/div/div/ul/li[1]/div/button[2]"
    
    element = driver.find_element(By.CLASS_NAME,"menu-toggle__store-name")
    element.click()
    time.sleep(4)

    error = True
    try:
        driver.find_element(By.CLASS_NAME,'store-locator-menu__location-toggle')
    except NoSuchElementException:
        error = False

    if error:
        element = driver.find_element(By.CLASS_NAME,"store-locator-menu__location-toggle")
        element.click()

    time.sleep(4)
    element = driver.find_element(By.CLASS_NAME,"location-form__field")
    time.sleep(4)
    element.clear()
    element.send_keys(zipcode)
    element = driver.find_element(By.CLASS_NAME,"location-form__apply-button")
    element.click()
    time.sleep(4)
    element = driver.find_element(By.XPATH, xpath)
    element.click()
    time.sleep(10)
    """

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    k = {}
    items = list()

    try:
        entry = soup.find_all("div", {"class" : "product-card__title"})
    except:
        entry = None

    for i in range (1,5):
        try:
            k["Item {}".format(i)] = entry[i].text
        except:
            k["Item{}".format(i)] = None
        items.append(k)
        k = {}

    links = list()
    images = soup.find_all ("img", {"src" : True})
    for img in images:
        links.append(img['src'])

    imageList2 = links[3:7]

    return (items)

def walgreenStore(input,zipcode):
    global imageList3

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    url = "https://www.walgreens.com/search/results.jsp?Ntt="
    inStock = "&inStockOnly=true"
    fullUrl = url + input + inStock

    driver.get(fullUrl)
    driver.maximize_window()
    time.sleep(20)

    #Location
    """
    element = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[1]/div[1]/span/div/div[1]/a/span")
    element.click()
    time.sleep(4)
    element = driver.find_element(By.ID, "store-header-search")
    element.click()
    element.send_keys(zipcode)
    element.send_keys(Keys.RETURN)
    time.sleep(7)
    element = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div[2]/ul/li[1]/div[2]/a")
    element.click()
    time.sleep(6)
    """

    soup = BeautifulSoup(driver.page_source,'html.parser')
    driver.close()

    k = {}
    items = list()

    try:
        entry = soup.find_all("strong", {"class":"description"})
    except:
        entry = None

    for i in range (0,4):
        try:
            k["Item {}".format(i+1)] = entry[i].text
        except:
            k["Item{}".format(i+1)] = None
        items.append(k)
        k = {}

    links = list()

    for images in soup.find_all("figure", {"class":"product__img"}):
        for img in images.find_all("img"):
            links.append(img['src'])

    tempString = "https://"
    newLinks = links[:4]
    newLinks = [re.sub("450.", "100.", i) for i in newLinks]
    imageList3 = [tempString + s for s in newLinks]

    return items



# """ def tristen_a3p3(request, *args, **kwargs):
#     return render(request, "tristena3p3.html", {})

# def ryleya3p3(request, *args, **kwargs):
#     return render(request, "ryleya3p3.html", {})	

# def ryana3p3(request, *args, **kwargs):
#     return render(request, "ryana3p3.html", {}) """

#def getResult(input):
#     global imageList

#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

#     itemSearch = input

#     dollarLink = "https://www.dollartree.com/searchresults?Ntt="
#     link  = dollarLink + itemSearch

#     driver.get(link)
#     driver.maximize_window()
#     time.sleep(7)
#     driver.execute_script("window.scrollTo(0,500);")
#     time.sleep(3)

#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     driver.close()
#     k = {}

#     """ #Walmart Test
#     #finding all the items on the page
#     try:
#         item = soup.find_all("span", {"class" : "w_V_DM"})
#     except:
#         item = None
    
#     #Only get the first 4 items
#     for i in range (0,4):
#         try:
#             k["Item{}".format(i + 1)] = item[i].find("span", {"data-automation-id": "product-title"}).text.replace("\n","")
#         except:
#             k["Item{}".format(i + 1)] = None
#     content.append(k)
#     k = {}
#     """

#     #Dollar Tree Testing
#     items = list()

#     try:
#         entry = soup.find_all("span", {"data-bind": "html: displayName"})
#     except:
#         entry = None

#     count = 1
#     for i in range(0, 8, 2):
#         try:
#             k["Item {}".format(count)] = entry[i].text
#         except:
#             k["Item{}".format(i + 1)] = None
#         items.append(k)
#         k = {}
#         count = count + 1

#     links = list()
#     for images in soup.find_all("img", {"class": "bg-product-image"}):
#         links.append(images['src'])

#     tempString = "https://www.dollartree.com"
#     newLinks = links[:4]
#     newLinks = [re.sub("=940", "=75", i) for i in newLinks]
#     newLinks = [tempString + s for s in newLinks]

#     imageList = newLinks
    
#     return (items)

# def getImage():
#     global imageList
#     return imageList



