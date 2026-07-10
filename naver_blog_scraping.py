from bs4 import BeautifulSoup
import requests
import re
import time
import sys
import os
import urllib.request
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
from dotenv import load_dotenv

# .env 파일 불러오기
load_dotenv() 

# 웹드라이버 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# 버전에 상관 없이 os에 설치된 크롬 브라우저 사용
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(3)
# 버전에 상관 없이 os에 설치된 크롬 브라우저 사용

# 환경 변수 접근하기
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

# selenium으로 검색 페이지 불러오기 #
naver_urls = []
postdate = []
titles = []

# 검색어 입력
keyword = input("검색할 키워드를 입력해주세요.") # 공연 이름으로 바꿔야 하는 부분
encText = urllib.parse.quote(keyword)

# 검색을 끝낼 페이지 입력
end = input("\n크롤링을 끝낼 위치를 입력해주세요. (기본값: 1, 최댓값: 100)") # 대극장 기준 리뷰 블로그 개수를 확인해보고 결정
if end == "":
    end = 1
else:
    end = int(end)
print("\n 1 ~ ", end, "페이지까지 크롤링을 진행합니다.")

# 한번에 가져올 페이지 입력
display = input("\n한번에 가쟈올 페이지 개수를 입력해주세요. (기본값 : 10, 최댓값 : 100)") # 검색을 끝낼 페이지 기준으로 결정
if display == "":
    display = 10
else:
    dispaly = int(display)
print("\n한번에 가져올 페이지 : ", display, "페이지")

for start in range(end):
    url = "https://openai.naver.com/v1/search/blog?query=" + encText + "&start=" + str(start+1) + "&display=" + str(display+1) # Json 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver_client-Id".client_id)
    request.add_header("X-Naver-Client-Secret".client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        data = json.loads(response_body.decode('urf-8'))['items']
        for row in data:
            if('blod.naver' in row['link']):
                naver_urls.append(row['link'])
                postdate.append(row['postdata'])
                title = row['title']
                # html 태그 제거
                pattern1 = '<[^>]*>'
                title = re.sub(pattern=pattern1, repl='', string=title)
                titles.append(title)
            time.sleep(2)
        else:
            print('Error Code: ' + rescode)