#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC#被動等待
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import re as re
import time
import pandas as pd


# In[ ]:


USERNAME = input("Enter the username: ")
PASSWORD = input("Enter the password: ")
print(USERNAME)
print(PASSWORD)


# In[ ]:



driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.linkedin.com/uas/login")
time.sleep(3)
email=driver.find_element_by_id("username")
email.send_keys(USERNAME)
password=driver.find_element_by_id("password")
password.send_keys(PASSWORD)
time.sleep(3)
password.send_keys(Keys.RETURN)

## 搜尋職缺地點與職稱
position = "data scientist"
local = "台灣"
position = position.replace(' ', "%20")
driver.get(f"https://www.linkedin.com/jobs/search/?geoId=104187078&keywords={position}&location={local}")

time.sleep(2)
disc_list = []

## 每頁職缺顯示的職缺數不一，透過迴圈確認有多少職缺在頁面上 
for i in range(1,41):
    ## 點選按鈕改變頁數
    driver.find_element_by_xpath(f'//button[@aria-label="第 {i} 頁"]').click()
    jobs_lists = driver.find_element_by_class_name('jobs-search-results__list') #建立職缺的陣列
    jobs = jobs_lists.find_elements_by_class_name('jobs-search-results__list-item')#計算職缺數
    time.sleep(1) 
    
    for job in range (1, len(jobs)+1):
        driver.find_element_by_xpath(f'/html/body/div[7]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li[{job}]/div/div[1]/div[1]/div[2]/div[1]/a').click() 
        time.sleep(1)
        job_desc = driver.find_element_by_class_name('jobs-search__right-rail')
        soup = bs(job_desc.get_attribute('outerHTML'), 'html.parser')
        disc_list.append(soup.text)


# In[ ]:


# 爬蟲整理
df = pd.DataFrame(disc_list)
df = df.replace(['\n',
                 '分享',
                 '更多選項',
                 '^.*?Expect', 
                 '^.*?Qualifications', 
                 '^.*?Required', 
                 '^.*?expected', 
                 '^.*?Responsibilities', 
                 '^.*?Requisitos', 
                 '^.*?Requirements', 
                 '^.*?Qualificações', 
                 '^.*?QualificationsRequired1', 
                 '^.*?você deve ter:', 
                 '^.*?experiência', 
                 '^.*?você:', 
                 '^.*?Desejável', 
                 '^.*?great', 
                 '^.*?Looking For', 
                 '^.*?ll Need', 
                 '^.*?Conhecimento', 
                 '^.*?se:',
                 '^.*?habilidades',                 
                 '^.*?se:',
                 '^.*?REQUISITOS'
                 ], '', regex=True)
df


# In[ ]:




