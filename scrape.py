from selenium import webdriver
import time
import sys
import os
import datetime
import random
import csv
import re
from nameparser import HumanName
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains



def getEnv():
    browser = webdriver.Firefox()
    return browser



def tearDown(browser):
    browser.close()
        
def getpolyvoreUserUrl(browser):
    polyvoreUserProfile = []
    polyvoreUserProfileLinks = []
    userBlogList = []
    userNameList = []
    browser.get('https://www.polyvore.com/fashion_lovers/group.show?id=176639&tab=members')
    
    try:
        timeout = time.time() + 60*5 # sec*min Ajax increase value to fetch more users
        while True:
            if time.time() > timeout:
                break
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            polyvoreUserProfile = browser.find_elements_by_class_name('clickable')
        print(len(polyvoreUserProfile))
    except NoSuchElementException:
        pass
    for elem in polyvoreUserProfile:
        if elem.get_attribute("href") is not None: # Filter the url data
            polyvoreUserProfileLinks.append(elem.get_attribute("href"))
    
    for user in polyvoreUserProfileLinks:
        browser.get(user)
        try:
            userBlog=browser.find_element_by_xpath('//*[@id="left"]/div/div[2]/div[4]/a[1]')
            userName = browser.find_element_by_xpath('//*[@id="left"]/div/div[2]/div[1]/h1/span')
            userBlogList.append(userBlog.get_attribute("href"))
        except:
            try:
                userBlog=browser.find_element_by_xpath('//*[@id="left"]/div/div[2]/div[4]/a')
                userName = browser.find_element_by_xpath('//*[@id="left"]/div/div[2]/div[1]/h1/span')
                userBlogList.append(userBlog.get_attribute("href"))
                
            except:
                pass
    print(userBlogList)
    print(len(userBlogList))
    csvfile = "info.csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for row in userBlogList:
            writer.writerow([row])
    return browser


def scrapeEMailsandNames(browser):

    with open('info.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        with open('output.csv', 'w') as csv_file:
            write_file = csv.writer(csv_file)
            write_file.writerow(["Urls", "Email", "Name"])
            for row in readCSV:
                print(row[0])
                browser.get(row[0])
                html = browser.page_source
                result = re.sub("<.*?>", "", html)
                email = re.findall(r'[\w\.-]+@[\w\.-]+', result)
                name = HumanName(result)
                row_data = [str(row[0]), str(email), str(name.first)]
                write_file.writerow(row_data)
    return browser
    

   
def main():
    browser=getEnv()
    browser=getpolyvoreUserUrl(browser)
    browser=scrapeEMailsandNames(browser)
    tearDown(browser)

    
	

if __name__ == '__main__':
    main()