from bs4 import Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import requests
from bs4 import BeautifulSoup

f = open('color_list_popular.txt','w')

# 使用chromedirver
chromedriver = '/usr/local/bin/chromedriver'





# for type in types:
url = 'https://colorhunt.co/palettes/popular'
driver = webdriver.Chrome(chromedriver)
driver.get(url)
time.sleep(10)

alltime_button = driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div[1]/div[3]')
alltime_button.click()

for i in range(1,5):
    js=f"var action=document.documentElement.scrollTop={i}0000"
    driver.execute_script(js)
    time.sleep(3)

for num in range(1,200):
    
    xpath = f'/html/body/div[4]/div[2]/div/div[{num}]/div[1]/div[1]/a'
    span = driver.find_elements(By.XPATH,xpath)
    for i in span:
        try:
            f.write(i.get_attribute('href')+'\n')
        except:
            pass



f.close()
time.sleep(10)
driver.quit()