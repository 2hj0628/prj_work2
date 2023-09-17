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
end_date = date(2021, 4, 20)

while start_date <= end_date :
    try :
        time.sleep(2)
        # 시작날짜 입력
        date_from=driver.find_element(By.XPATH,'//*[@id="sSearchFrom"]')

        for i in range(10):
            date_from.send_keys(Keys.BACKSPACE) 

        date_from.send_keys(start_date.strftime("%Y-%m-%d")) 

        # 종료날짜 입력
        date_to=driver.find_element(By.XPATH,'//*[@id="sSearchTo"]')

        for i in range(10):
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
                       
        #전체 차트 수집하기         
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

        for i in content_column :
            column_list.append(i.text.replace("\t","").replace("\n","").replace("오름차순내림차순",""))
        print(column_list)
        
        # 항목 리스트 생성
        rank_table=soup.find('tbody').find_all('tr')

        rank_list=[]
        
        #리스트에 항목 담기
        for movie in rank_table :
            chart=[]
            chart.append(search_date)

            #영화 순위
            movie_rank=movie.find('td').text.replace("\t","").replace("\n","")
            chart.append(movie_rank)

            #영화제목
            movie_title=movie.find('span','ellip per90').get_text()
            chart.append(movie_title)
            
            #개봉일
            movie_chart=movie.select('td:nth-child(3)')
            for i in movie_chart :
                chart.append(i.text.replace("\n","").replace("\t","").replace(" ",""))

            #'매출액', '매출액점유율', '매출액증감(전일대비)', '누적매출액', '관객수' 등
            movie_chart=movie.find_all('td','tar')

            for i in movie_chart :
                chart.append(i.text.replace("\t","").replace("\n",""))

            rank_list.append(chart)
            
        print(rank_list)
        
         # 영화별 세부정보 수집하기
        movie_name_list=soup.find_all('span','ellip per90')

        movie_info_cont=[]
        movie_staff=[]
        for i in movie_name_list :
            try :
                name=i.get_text()
                time.sleep(1)

                # 영화 정보 팝업 띄우기
                movie_btn=driver.find_element(By.LINK_TEXT,str(name))
                movie_btn.click()
                time.sleep(1)

                #영화 정보 가져오기
                movie_html=driver.page_source
                soup=BeautifulSoup(movie_html, 'html.parser')

                #영화제목
                movie_name=soup.find('div','hd_layer').find('strong').get_text()

                #영화세부정보contents
                movie_contents=soup.find('dl',class_='ovf cont').find_all('dd')
                
                movie_info=[]
                movie_info.append(movie_name)
            
                for cont in movie_contents :
                    movie_info.append(cont.text.replace("\n","").replace("\t","").replace(" ","").strip())
                
                movie_info_cont.append(movie_info)
                
                #감독, 배우 정보 수집
                try : 
                    movie_staff_dict={'감독' : [],'배우' : []}

                    director=soup.find('div','staffMore').find('dd').text.strip()
                    movie_staff_dict['감독'].append(director)

                    actor_list=soup.find('div','staffMore').find('td').find_all('a')

                    for i in actor_list :
                        movie_staff_dict['배우'].append(i.text.strip())
                        
                except : 
                    movie_staff_dict={'감독' : [],'배우' : []}
                    
                movie_staff.append(movie_staff_dict)

                # 팝업 창 닫기
                time.sleep(1)
                driver.find_element(By.LINK_TEXT,"뒤로").click()
                
            except : 
                print("오류 항목을 제외합니다.")
                continue
                
        print(movie_info_cont)
        print(movie_staff)
            
    except :
        print("데이터를 수집하지 못하였습니다.")
        break

# print(search_total)
# print(column_list)
# print(rank_list)
# print(movie_info_tit)
# print(movie_info_cont)
# print(movie_staff)


# kobis 데이터 수집 종료
print()
print("<KOBIS 일별 박스오피스 크롤링이 완료되었습니다.>")
print()
print("----------------------------------------------------------------")