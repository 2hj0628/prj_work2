##네이버 리뷰 수집

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import xlwt
import os
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
from selenium.webdriver.chrome.service import Service


##디버거 크롬
datadir=os.getcwd()+r'\chrometemp'    
try:
    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="'+datadir+r'"') 
except:
    subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="'+datadir+r'"')
option=Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

#크롬 버전확인하여 chromedriver 설치하고 구동
chrome_ver=chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver=webdriver.Chrome(service=Service(f'./{chrome_ver}/chromedriver.exe'), options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver=webdriver.Chrome(service=Service(f'./{chrome_ver}/chromedriver.exe'), options=option)
#html페이지소스 전체로딩후 연결, 최대10초 대기
driver.implicitly_wait(10)
#크롤링할 페이지 연결
url="https://movie.naver.com/movie/point/af/list.naver"
driver.get(url)


print("----------------------------------------------------------------")

print("<네이버 영화리뷰 크롤링을 시작합니다.>")
print()
full_html=driver.page_source    
soup=BeautifulSoup(full_html,'html.parser')

##게시물 수
content_num=soup.find_all('div','h5_right_txt')

for i in content_num:
    txt2=i.get_text().strip()
print(txt2)


#추출데이터 누적할 변수
movie_num_txt=[]
movie_name_txt=[]
review_txt=[]
list_netizen_score_txt=[]
whole_score_txt=[]
date_txt=[]


num=0

#데이터 추출
for page in range(1,2000):
        
    
    full_html=driver.page_source    
    soup=BeautifulSoup(full_html,'html.parser')

    ##리뷰 번호
    movie_num=soup.find_all('td','ac num')

    for i in movie_num:
        txt=i.get_text().strip()
        num+=1
        movie_num_txt.append(txt)
    print(movie_num_txt)

    ##영화 이름
    movie_name=soup.find_all('a','movie color_b')

    for i in movie_name:
        txt=i.get_text().strip()
        num+=1
        movie_name_txt.append(txt)
    print(movie_name_txt)

    ##리뷰
    reviews = soup.find_all("td",{"class":"title"})
    for i in reviews:
        sentence = i.find("a",{"class":"report"}).get("onclick").split("', '")[2]
        #만약 리뷰 내용이 비어있다면 데이터를 사용하지 않음
        # if sentence != "":
        review_txt.append([sentence])
    print(review_txt)

    ##별점
    list_netizen_score=soup.find_all('div','list_netizen_score')

    for i in list_netizen_score:
        txt=i.get_text().strip()
        new_txt = txt.replace('별점 - 총 10점 중', '')
        num+=1
        list_netizen_score_txt.append(new_txt)
    print(list_netizen_score_txt)

    ##총 별점
    whole_score='10'
    for i in list_netizen_score:
        num+=1
        whole_score_txt.append(whole_score)
    print(whole_score_txt)



    ##날짜--아직 못함
    date=soup.select("td:nth-child(3)")
    for i in date:
        txt=i.get_text().strip()

        num+=1
        date_txt.append(txt)
        
    print(date_txt)

    ##페이지 넘기기
    page+=1    
    driver.find_element(By.LINK_TEXT, str(page)).send_keys(Keys.ENTER)        

    time.sleep(3)

#총 리뷰 개수만 추출
txt3=txt2.replace('총', '').replace('개의 평점이 있습니다.', '')
print("<총",txt3,"건 수집완료 되었습니다.>")
print()
print("<네이버 리뷰 크롤링이 완료되었습니다.>")
print()
print("----------------------------------------------------------------")