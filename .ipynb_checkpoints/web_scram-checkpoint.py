from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

# 使用chromedirver
chromedriver = '/usr/local/bin/chromedriver'

# 使用內政部網站
url = 'http://plvr.land.moi.gov.tw/DownloadOpenData'


driver = webdriver.Chrome(chromedriver)
driver.get(url)
time.sleep(2)

# 點擊非本期下載
unnow_button = driver.find_element(By.ID,'ui-id-2')
unnow_button.click()
time.sleep(2)

# 點擊進階下載
moreinfo_button = driver.find_element(By.ID,'downloadTypeId2')
moreinfo_button.click()
time.sleep(2)

# 選取發布日期
season_select = driver.find_element(By.CSS_SELECTOR,'#historySeason_id')
Select(season_select).select_by_index(12)
time.sleep(2)

# 選擇台北
taipei_button = driver.find_element(By.CSS_SELECTOR,'#table5 > tbody > tr:nth-child(7) > td:nth-child(2) > input')
taipei_button.click()
time.sleep(2)

# 選擇新北
newtpe_button = driver.find_element(By.CSS_SELECTOR,'#table5 > tbody > tr:nth-child(8) > td:nth-child(2) > input')
newtpe_button.click()
time.sleep(2)

# 選擇桃園
taoyuan_button = driver.find_element(By.CSS_SELECTOR,'#table5 > tbody > tr:nth-child(9) > td:nth-child(2) > input')
taoyuan_button.click()
time.sleep(2)

# 選擇台中
taichun_button = driver.find_element(By.CSS_SELECTOR,'#table5 > tbody > tr:nth-child(13) > td:nth-child(2) > input')
taichun_button.click()
time.sleep(2)

# 選擇高雄
kaoshun_button = driver.find_element(By.CSS_SELECTOR,'#table5 > tbody > tr:nth-child(20) > td:nth-child(2) > input')
kaoshun_button.click()
time.sleep(2)

# 選擇CSV方式
season_select = driver.find_element(By.CSS_SELECTOR,'#fileFormatId')
Select(season_select).select_by_index(2)
time.sleep(2)

# 點擊下載
download_button = driver.find_element(By.CSS_SELECTOR,'#downloadBtnId')
download_button.click()

time.sleep(10)

driver.quit()