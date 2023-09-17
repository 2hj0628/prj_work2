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

#kobis 데이터 수집 시작
print("----------------------------------------------------------------")
print("<KOBIS 일별 박스오피스 크롤링을 시작합니다.>")
print()

# KOBIS (일별 박스오피스) 페이지 접속하기
path = "C:\\web_driver\\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://www.kobis.or.kr/kobis/business/stat/boxs/findDailyBoxOfficeList.do")
time.sleep(3)

# 데이터 수집 기간 설정하기
start_date = date(2020, 10, 21)
end_date = date(2022, 10, 20)

rank_list=[]
movie_info_cont=[]

#전체 차트 수집하기(rank_list=[])
while start_date <= end_date :
    try :
        # 검색 시작날짜 입력
        date_from=driver.find_element(By.XPATH,'//*[@id="sSearchFrom"]')
        for i in range(10):
            date_from.send_keys(Keys.BACKSPACE) 
        date_from.send_keys(start_date.strftime("%Y-%m-%d")) 

        # 검색 종료날짜 입력
        date_to=driver.find_element(By.XPATH,'//*[@id="sSearchTo"]')
        for j in range(10):
            date_to.send_keys(Keys.BACKSPACE)
        date_to.send_keys(start_date.strftime("%Y-%m-%d"))

        # 조회 버튼 클릭
        search_btn=driver.find_element(By.XPATH,'//*[@id="searchForm"]/div/div[5]/button')
        search_btn.click()
        time.sleep(1)

        # 검색일자 업데이트
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

        # 데이터 해당 날짜 
        search_date=soup.find('div','board_tit').get_text().replace("\n","")

        # 일별 검색건수
        search_total=soup.find('em','fwb').get_text()
        # print(search_total)

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

            #영화제목
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

        #확인용 rank_list 출력    
        # print(rank_list)
        
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

                    #영화제목
                    movie_name=soup.find('div','hd_layer').find('strong').get_text()
                    movie_info.append(movie_name)

                    #영화세부정보contents
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

                    #확인용 movie_info_cont 출력
                    # print(movie_info_cont)

                    # 팝업 창 닫기
                    time.sleep(1)
                    driver.find_element(By.LINK_TEXT,"뒤로").click()
                    
            except : 
                print("오류 항목을 제외합니다.")
                continue

    except :
        print("데이터를 수집하지 못하였습니다.")
        break

#csv 파일로 저장
kobis_rank=pd.DataFrame()
kobis_rank["영화순위"]=rank_list
kobis_rank.to_csv("kobis_rank.csv", encoding='utf-8-sig', index=False)

kobis_movie_info=pd.DataFrame()
kobis_movie_info["영화상세정보"]=movie_info_cont
kobis_movie_info.to_csv("kobis_movie_info.csv", encoding='utf-8-sig', index=False)