# 1. 네이버 블로그 상세 url 함수 만들기
import urllib.request    # 웹요청 모듈 
from bs4 import BeautifulSoup    # html 파싱 모듈 
from selenium import webdriver   # 브라우저 제어 모듈 
from selenium.webdriver.chrome.service import Service   # 드라이버 관리 모듈 
from selenium.webdriver.common.by import By     # 요소 탐색 모듈 
import time    # 대기 시간 정해주는 모듈 
from selenium.webdriver.chrome.options import Options
import subprocess
from selenium_stealth import stealth

def  naver_blog(keyword, n):

## 자동 시스템에 의해 제어되는 것을 막기 위한 코드 부분 ## 

    option = Options()
    driver = webdriver.Chrome(options=option)

    stealth(driver,
        languages=['en-US', 'en'],
        vendor='Google Inc.',
        platform='Win64',
        webgl_vendor='Intel Inc.',
        renderer='Intel Iris OpenGL Engine',
        fix_hairline=True)

## -------------------------------------------- ## 

    params = []  # 네이버 블로그의 상세 url을 담는 리스트
    for i in range(1,  n+1): # 페이지 번호 숫자 제공
        time.sleep(1) # 블로그에 사진이 많을 경우, 로딩이 오래 걸리므로 대기 시간 부여
        text1 = urllib.parse.quote(keyword) # 검색 키워드 가져옴

        # 블로그에 특정 키워드 검색 + 페이지 단위로 구분 -> 해당 페이지에 있는 블로그 글의 상세 주소를 저장하기 위한 것
        list_url="https://section.blog.naver.com/Search/Post.naver?pageNo=" + str(i) + "&rangeType=ALL&orderBy=sim&keyword=" + text1

        # 해당 웹 페이지를 열음 
        driver.get(list_url)
        time.sleep(2) 

        # 열린 블로그 리스트의 html을 가져옴
        html = driver.page_source

        # html 코드를 BS 으로 파싱함 
        soup = BeautifulSoup(html, "lxml") # html.parser 또는 lxml 을 사용

        # 상세 url(블로그 글 한 개의 url)을 찾음 
        for i in soup.select('div.desc > a.desc_inner'):
            params.append(i.get("href"))

    return params # 최종적으로 블로그 글 한 개 한 개의 url을 모두 담은 리스트를 반환함
    
# 2. 네이버 블로그 글과 상세 내역 파일 저장
def naver_blog2(keyword, n):
    # 첫번째 함수를 실행해서 상세 url 리스트 가져오기
    result = naver_blog(keyword, n)
    
    # 상세 글을 열기 위한 driver
    option = Options()
    driver2 = webdriver.Chrome(options=option)

    # 본문을 저장할 파일을 생성
    f2 = open("C:/Users/SSAFY/OneDrive/Desktop/SSAFY/my_pjt/muplay_recommendation_service/naver_blog.txt", "w", encoding="utf8")

    # 상세 url 을 하나씩 가져와서 여는 부분
    for  list_url  in  result:
        driver2.get(list_url)
        time.sleep(2)  # 페이지 로드 대기 시간 

        # 자바 스크립트로 막혀 있을 지도 모를 html 코드를 보게 하는 부분
        # 웹페이지에서 ID 가 'mainFrame' 인 HTML 요소를 찾음
        # mainFrame 의 html 코드가 독립적으로 작동되는 코드이기 때문임
        # 크롬 개발자 모드에서 iframe 태그를 찾음

        try:
            element = driver2.find_element(By.ID, 'mainFrame') # mainFrame 찾음 
            driver2.switch_to.frame(element) 
            # 현재 페이지의 html 코드를 가져옴
            html = driver2.page_source
            # BS 으로  html 코드를 파싱함
            soup = BeautifulSoup(html, "html.parser")

            # 날짜 검색
            date2 = soup.select("span.se_publishDate.pcol2")
            # 본문 검색
            base2 = soup.select("div.se-module.se-module-text > p")

            # 날짜만 추출
            # print(date2[0].text.strip()) 
            date_text = date2[0].text.strip()
            print(date_text)
            f2.write(date_text + '\n' )   
            
            # 본문 추출
            for i in base2:
                con_text = i.text.strip()
                print(con_text) 
                f2.write(con_text + '\n')
                
            print('\n\n\n')
            f2.write('\n' + '='*50 + '\n\n')
            
        except Exception  as  e:
            print('iframe 을 찾을 수 없습니다.', e)

    f2.close()  # 텍스트를 파일에 저장
    

naver_blog2("뮤지컬 레베카", 10)