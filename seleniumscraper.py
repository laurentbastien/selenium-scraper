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
#jobs
myinput = []
#names of individuals
mynames = []
#companies of the individuals 
companynames = []
#companies for second table
mycompanies = []
#industries for second table
targetedindustries = []
for i in [x for x in range(13) if x > 0]:
    sleep(3)
    browser.get("https://lobbycanada.gc.ca/app/secure/ocl/lrs/do/rcntRgstrns?rt=1&lang=eng&pg="+str(i))
    sleep(3)
    for i in [x for x in range(50) if x > 0]:
        sleep(4)
        element = browser.find_element_by_xpath("/html/body/div[1]/div/div[6]/div[2]/div[2]/div[4]/ol/li["+str(i)+"]/div/span[2]/a")
        element.location_once_scrolled_into_view
        browser.find_element_by_xpath("/html/body/div[1]/div/div[6]/div[2]/div[2]/div[4]/ol/li["+str(i)+"]/div/span[2]/a").click()
        sleep(3)                       
        browser.find_element_by_xpath('//*[@id="tab-trends"]/a/*').click()
        if browser.find_elements_by_link_text("Public offices held"):
            myurl = browser.current_url
            html = requests.get(myurl)
            page = html.text
            soup = BeautifulSoup(page, 'html.parser')
            #companies
            temporarycompanies = []
            companies = soup.find_all("h2")[1]
            for company in companies:
                company = str(company)
                company = company.replace("<li>","")
                company = company.replace("</li>","")
                company = company.strip()
                temporarycompanies.append(company)
            company = str(temporarycompanies)[0:str(temporarycompanies).find('/')]
            company = company.replace("[", "")
            company = company.replace("'", "")
            #industries
            temporaryindustries = []
            industries = soup.find_all("ul", {'class':'noIndent2'})[3]
            for industry in industries:
                industry = str(industry)
                industry = industry.replace("<li>","")
                industry = industry.replace("</li>","")
                industry = industry.strip()
                temporaryindustries.append(industry)
            industry = list(filter(None, temporaryindustries))
            industrycounter = len(industry)
            targetedindustries.extend(industry)
            company2 = [company] * industrycounter
            mycompanies.extend(company2)
            counter = len(browser.find_elements_by_link_text("Public offices held"))
            for i in range(counter):
                mylist = browser.find_elements_by_link_text("Public offices held")
                sleep(4)
                mylist[i].click()
                sleep(4)
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
                secondcounter = len(soup.findAll("td")[0::3])
                mynames.extend([name] * secondcounter)
                companynames.extend([company] * secondcounter)
                browser.find_element_by_xpath("/html/body/div/div/div[6]/a[2]").click()
                sleep(3)
                browser.find_element_by_xpath('//*[@id="tab-trends"]/a/strong').click()
                sleep(3) 
            browser.find_element_by_xpath("//*[@id='cn-centre-col-inner']/a[2]").click()
        else:
            sleep(4)
            browser.find_element_by_xpath("//*[@id='cn-centre-col-inner']/a[2]").click()
            sleep(3)
