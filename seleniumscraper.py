from selenium import webdriver
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from time import sleep
path_to_chromedriver = '/Users/laurentbastien/Desktop/home/practice/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
url = 'https://lobbycanada.gc.ca/app/secure/ocl/lrs/do/rcntRgstrns?lang=eng'
browser.get(url)
myinput = []
mynames = []
for i in [x for x in range(50) if x > 0]:
    sleep(4)
    element = browser.find_element_by_xpath("/html/body/div[1]/div/div[6]/div[2]/div[2]/div[4]/ol/li["+str(i)+"]/div/span[2]/a")
    element.location_once_scrolled_into_view
    browser.find_element_by_xpath("/html/body/div[1]/div/div[6]/div[2]/div[2]/div[4]/ol/li["+str(i)+"]/div/span[2]/a").click()
    sleep(3)                       
    browser.find_element_by_xpath('//*[@id="tab-trends"]/a/*').click()
    if browser.find_elements_by_xpath("//*[@id='trends-enhanced']/div/ul/li[*]/a"):
        counter = len(browser.find_elements_by_xpath("//*[@id='trends-enhanced']/div/ul/li[*]/a"))
        for i in range(counter):
            mylist = browser.find_elements_by_xpath("//*[@id='trends-enhanced']/div/ul/li[*]/a")
            sleep(4)
            mylist[i].click()
            sleep(3)
            myurl = browser.current_url
            html = requests.get(myurl)
            page = html.text
            soup = BeautifulSoup(page, 'html.parser')
            for div in soup.findAll("title"):
                name = [text for text in div.stripped_strings]
                name = str(name)
            name = name.replace("'Public offices held:", "")
            name = name.replace("\\r\\n", "")
            name = name.replace("\\t\\t\\t ", "")
            name = name.replace("Lobbyists Registration System -Office of the Commissioner of Lobbying of Canada'", "")
            name = name.replace("-", "")
            name = name.replace(" ", "")
            name = re.sub(r"(\w)([A-Z])", r"\1 \2", name)
            for div in soup.findAll("td"):
                myinput.append([str(text) for text in div.stripped_strings])
                mynames.append(name)
            browser.find_element_by_xpath("/html/body/div/div/div[6]/a[2]").click()
            sleep(3)
            browser.find_element_by_xpath('//*[@id="tab-trends"]/a/strong').click()
            sleep(3) 
        browser.find_element_by_xpath("//*[@id='cn-centre-col-inner']/a[2]").click()
    else:
        sleep(4)
        browser.find_element_by_xpath("//*[@id='cn-centre-col-inner']/a[2]").click()
        sleep(3)