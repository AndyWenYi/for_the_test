from bs4 import Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import requests
from bs4 import BeautifulSoup

# url = 'https://colorhunt.co/'
# res = requests.get(url,timeout=2.0,allow_redirects=False)
# soup = BeautifulSoup(res.text, "html.parser")
# # soup.find_all('div','class'=='item')
# # soup.find_all('span')
# # for i in soup.find_all('a'):
#     # print(i.get('href'))
# types = []
# for i in soup.find_all('a'):
#     try:
#         if '/palettes/' in i['href']:
#             types.append(i['href'])
#             # print(i['href'])
#     except:
#         pass
f = open('color_list_popular.txt','w')

# 使用chromedirver
chromedriver = '/usr/local/bin/chromedriver'

# 使用內政部網站




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
# for i in span:
# print(span)
    for i in span:
        # print(i.get_attribute('href'))
        try:
            f.write(i.get_attribute('href')+'\n')
        except:
            pass



f.close()
time.sleep(10)
driver.quit()

# /html/body/div[4]/div[2]/div/div[2]/div[1]/div[1]/a
# /html/body/div[4]/div[2]/div/div[32]/div[1]/div[1]/a

# /html/body/div[4]/div[2]/div/div[2]/div[1]/div[1]/a
# /html/body/div[4]/div[2]/div/div[3]/div[1]/div[1]/a
# /html/body/div[4]/div[2]/div/div[642]/div[1]/div[1]/a
# /html/body/div[4]/div[2]/div/div[643]/div[1]/div[1]/a
# /html/body/div[4]/div[2]/div/div[762]/div[1]/div[1]/a
# /html/body/div[4]/div[2]/div/div[803]/div[1]/div[1]/a
# /html/body/div[4]/div[2]/div/div[802]/div[1]/div[1]/a
# /html/body/div[4]/div[2]/div/div[802]/div[1]/div[1]/a