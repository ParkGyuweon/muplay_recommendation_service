from selenium import webdriver 
from bs4 import BeautifulSoup 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
import subprocess

main_url = "https://nol.yanolja.com/ticket" # 인터파크 티켓 메인 사이트
keyword = "뮤지컬" # 자동으로 검색창에 입력할 키워드

## 자동 시스템에 의해 제어되는 것을 막기 위한 코드 부분 ## 

subprocess.Popen('C:/Program Files/Google/Chrome/Application/chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=option)
driver.get(main_url)

stealth(driver,
        languages=['en-US', 'en'],
        vendor='Google Inc.',
        platform='Win64',
        webgl_vendor='Intel Inc.',
        renderer='Intel Iris OpenGL Engine',
        fix_hairline=True)

## -------------------------------------------- ## 

search = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/header/div/div[1]/div/div[1]/form/input')
search.send_keys(keyword)
search.send_keys(Keys.ENTER)