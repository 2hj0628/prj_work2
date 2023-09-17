from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from datetime import date,datetime,timedelta
import time
import sys
import os
import pandas as pd
import xlwt

import requests
import sqlite3 as sql
import pymysql
import re

#kobis 데이터 수집 시작
print("----------------------------------------------------------------")
print("<KOBIS 일별 박스오피스 크롤링을 시작합니다.>")
print()

# KOBIS (일별 박스오피스) 페이지 접속하기
path = "C:\\web_driver\\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://www.kobis.or.kr/kobis/business/stat/boxs/findDailyBoxOfficeList.do")
time.sleep(3)

# 날짜 입력 후 조회하기
start_date = date(2020, 10, 20)
end_date = date(2020, 10, 21)

rank_list=[]
movie_info_cont=[]

#전체 차트 수집하기(rank_list=[])
while start_date <= end_date :
    try :
        # 시작날짜 입력
        date_from=driver.find_element(By.XPATH,'//*[@id="sSearchFrom"]')
        for i in range(10):
            date_from.send_keys(Keys.BACKSPACE) 
        date_from.send_keys(start_date.strftime("%Y-%m-%d")) 

        # 종료날짜 입력
        date_to=driver.find_element(By.XPATH,'//*[@id="sSearchTo"]')
        for j in range(10):
            date_to.send_keys(Keys.BACKSPACE)
        date_to.send_keys(start_date.strftime("%Y-%m-%d"))

        # 조회 버튼 클릭
        search_btn=driver.find_element(By.XPATH,'//*[@id="searchForm"]/div/div[5]/button')
        search_btn.click()
        time.sleep(1)

        start_date+=timedelta(days=1)

        #더보기 클릭하여 전체 자료보기
        while True :
            try :
                driver.find_element(By.LINK_TEXT,"더보기").click()
            except :
                break
        
        # 페이지 읽어오기       
        full_html=driver.page_source
        soup=BeautifulSoup(full_html, 'html.parser')

        # 검색날짜 
        search_date=soup.find('div','board_tit').get_text().replace("\n","")

        # 검색건수
        search_total=soup.find('em','fwb').get_text()
        print(search_total)

        # 컬럼 리스트 생성
        content_column=soup.find('thead').find_all('th',{'scope':'col'})
        column_list=[]
        column_list.append('일자')
        for column in content_column :
            column_list.append(column.text.replace("\t","").replace("\n","").replace("오름차순내림차순",""))
        print(column_list)

        # 항목 리스트 생성
        rank_table=soup.find('tbody').find_all('tr')

        #리스트에 항목 담기
        for movie in rank_table :
            chart=[]
            chart.append(search_date)

            #영화 순위
            movie_rank=movie.find('td').text.replace("\t","").replace("\n","")
            chart.append(movie_rank)

            #영화 랭킹 - 영화제목
            movie_title=movie.find('span','ellip per90').get_text()
            chart.append(movie_title)

            #개봉일
            movie_chart=movie.select('td:nth-child(3)')
            for date in movie_chart :
                chart.append(date.text.replace("\n","").replace("\t","").replace(" ",""))

            #'매출액', '매출액점유율', '매출액증감(전일대비)', '누적매출액', '관객수' 등
            movie_chart=movie.find_all('td','tar')
            for record in movie_chart :
                chart.append(record.text.replace("\t","").replace("\n",""))

            rank_list.append(chart)
            
        print(rank_list)
        
# 영화별 세부정보 수집하기 (movie_info_cont=[])
        movie_name_list=soup.find_all('span','ellip per90')
        for k in movie_name_list :
            try :
                name=k.get_text()

                # 영화 정보 팝업 띄우기
                movie_info=[]
                
                if all(name not in movie_info for movie_info in movie_info_cont):
                    movie_btn=driver.find_element(By.LINK_TEXT,str(name))
                    movie_btn.click()
                    time.sleep(1)

                    #영화 정보 가져오기
                    movie_html=driver.page_source
                    soup=BeautifulSoup(movie_html, 'html.parser')

                    #영화 세부정보- 영화제목
                    movie_name=soup.find('div','hd_layer').find('strong').get_text()
                    movie_info.append(movie_name)

                    #영화세부정보 - contents
                    movie_contents=soup.find('dl',class_='ovf cont').find_all('dd')
                    for cont in movie_contents :
                        movie_info.append(cont.text.replace("\n","").replace("\t","").replace(" ","").strip())

                    #감독, 배우 정보 수집
                    try : 
                        movie_staff_dict={'감독' : [],'배우' : []}
                        director=soup.find('div','staffMore').find('dd').text.strip()
                        movie_staff_dict['감독'].append(director)
                        actor_list=soup.find('div','staffMore').find('td').find_all('a')
                        for actor in actor_list :
                            movie_staff_dict['배우'].append(actor.text.strip())
                        movie_info.append(movie_staff_dict)

                    except : 
                        movie_staff_dict={'감독' : [],'배우' : []}
                        movie_info.append(movie_staff_dict)
                    
                    #영화제목,세부정보,감독,배우 movie_info_cont 리스트에 담기
                    movie_info_cont.append(movie_info)
                    print(movie_info_cont)

                    # 팝업 창 닫기
                    time.sleep(1)
                    driver.find_element(By.LINK_TEXT,"뒤로").click()
                    
            except : 
                print("오류 항목을 제외합니다.")
                continue

    except :
        print("데이터를 수집하지 못하였습니다.")
        break

driver.close()

# 데이터 저장을 위한 컬럼 별 리스트 생성

gid_k=[]
gmovie_k=[]
gmovie2_k=[]
gdate_k=[]

gaudience=[]
ggenre=[]
gopendate=[]
gdirec=[]
gactor=[]
gmovie_id=[]

gdate1=[]
gdate2=[]
ggenre1=[]

for i in range(len(rank_list)):
    gid_k.append(i+1)  #번호
    gmovie_k.append(rank_list[i][2])  #영화제목
    gaudience.append(int(rank_list[i][8].replace(",","")))  #관객수
    
    gdate1.append(rank_list[i][0])
    gdate2=re.findall('\d+',gdate1[i])
    gdate_k.append('-'.join(gdate2))  #날짜
    
    if len(rank_list[i][3])==10:
        gopendate.append(rank_list[i][3])  #개봉일
    else:
        gopendate.append('1111-11-11')  #개봉일 데이터 없을시 1111-11-11로 통일
        
for i in range(len(movie_info_cont)):
    gmovie2_k.append(movie_info_cont[i][0])   #영화세부정보 - 영화제목
    gmovie_id.append(movie_info_cont[i][1])  #코드(식별코드)
    ggenre1.append(movie_info_cont[i][4].split('|'))
    
for i in range(len(ggenre1)):
    ggenre.append(ggenre1[i][2])  #장르
    
for i in range(len(movie_info_cont)) :   #감독, 배우
    if len(str(list(movie_info_cont[i][-1]['감독'])).replace("'","").replace("[","").replace("]",""))>0 :
        gdirec.append(str(list(movie_info_cont[i][-1]['감독'])).replace("'","").replace("[","").replace("]",""))
        gactor.append(str(list(movie_info_cont[i][-1]['배우'])).replace("'","").replace("[","").replace("]",""))
    else :
        gdirec.append("Null")
        gactor.append("Null")


#csv 파일로 저장하기

#영화 일별 박스오피스 csv 파일
kobis_rank=pd.DataFrame()
kobis_rank['번호']=gid_k
kobis_rank['날짜']=gdate_k
kobis_rank['영화제목']=gmovie_k
kobis_rank['관객수']=gaudience
kobis_rank['개봉일']=gopendate

#영화 별 정보 csv 파일
kobis_movie=pd.DataFrame()
kobis_movie['영화제목']=gmovie2_k
kobis_movie['코드']=gmovie_id
kobis_movie['장르']=ggenre
kobis_movie['감독']=gdirec
kobis_movie['주연배우']=gactor

kobis_rank.to_csv('kobis_rank.csv',encoding='utf-8-sig',index=False)
kobis_movie.to_csv('kobis_movie.csv',encoding='utf-8-sig',index=False)