import subprocess
import sys

try:
    import selenium
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from bs4 import BeautifulSoup
    import pandas as pd
    import xlwt
    from selenium.webdriver.chrome.options import Options
    import chromedriver_autoinstaller
    from selenium.webdriver.chrome.service import Service
except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'selenium'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'bs4'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pandas'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'xlwt'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'chromedriver_autoinstaller'])
    
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
url1="https://movie.naver.com/movie/point/af/list.naver"
driver.get(url1)

print("----------------------------------------------------------------")
print("< NAVER 영화리뷰 크롤링을 시작합니다.>")
print()

#추출데이터 누적할 리스트
movie_num_txt=[]  #리뷰번호
movie_name_txt=[]  #영화제목
review_txt=[]  #리뷰내용
list_netizen_score_txt=[]  #네티즌 별점
whole_score_txt=[]  #영화 총 별점
date_txt=[]  #리뷰작성일자
movie_tscore=[]  #영화제목+총별점

#페이지 읽어오기
full_html=driver.page_source    
soup=BeautifulSoup(full_html,'html.parser')

##게시물 수 : txt2
content_num=soup.find_all('div','h5_right_txt')
for num1 in content_num:
    txt2=num1.get_text().strip()
print(txt2)

#데이터 추출
for page in range(1,6):  #500개 크롤링
        
    full_html=driver.page_source    
    soup=BeautifulSoup(full_html,'html.parser')

    ##리뷰 번호  : movie_num_txt[]
    movie_num=soup.find_all('td','ac num')
    for review_num in movie_num:
        txt=review_num.get_text().strip()
        movie_num_txt.append(txt)

    ##영화 이름 : movie_name_txt[]
    movie_name=soup.find_all('a','movie color_b')
    for name in movie_name:
        txt=name.get_text().strip()
        movie_name_txt.append(txt)

    ##리뷰내용 : review_txt[]
    reviews = soup.find_all("td",{"class":"title"})
    for txt in reviews:
        sentence = txt.find("a",{"class":"report"}).get("onclick").split("', '")[2]
        #만약 리뷰 내용이 비어있다면 데이터를 사용하지 않음
        # if sentence != "":
        # review_txt.append([sentence])
        review_txt.append(sentence)   #22.11.07고정원수정

    ##리뷰별점 : list_netizen_score_txt[]
    list_netizen_score=soup.find_all('div','list_netizen_score')
    for score in list_netizen_score:
        txt=score.get_text().strip()
        new_txt = txt.replace('별점 - 총 10점 중', '')
        list_netizen_score_txt.append(new_txt)

    ##리뷰작성일자 : date_txt[]
    date=soup.select("td:nth-child(3)")
    for rd in date:
        txt=rd.get_text().strip()[-8:]
        txt='20'+txt.replace('.','-')
        date_txt.append(txt)      #22.11.07 이호제 수정

    ##총 별점    #22.11.07 고정원 수정(영화의 총 평점이 아니므로 사용하지 않음)
    # whole_score='10'
    # for i5 in list_netizen_score:
    #     whole_score_txt.append(whole_score)
    # print(whole_score_txt)

    ##영화 총 별점 추출하기 : whole_score_txt[] 
    for name in movie_name_txt:          
        if name in movie_tscore:
            movie_tscore.append(name)
            movie_tscore.append(movie_tscore[movie_tscore.index(name)+1])
            time.sleep(0.5)
        else:
            # time.sleep(0.5)
            #영화 총점 조회 페이지로 넘어가기
            movie_btn=driver.find_element(By.LINK_TEXT,name)
            movie_btn.click()
            # time.sleep(1)
            time.sleep(0.5)
            #바뀐 페이지 읽어오기
            movie_html=driver.page_source    
            movie_soup=BeautifulSoup(movie_html,'html.parser')
            score_movie=movie_soup.find('tbody').find('strong')
            movie_tscore.append(name)    #영화제목
            movie_tscore.append(score_movie.get_text().replace('/','').replace('10','').strip())   #해당영화의 총 별점

            time.sleep(0.5)
            driver.back()
            # time.sleep(0.5)
        
    ##페이지 넘기기
    driver.find_element(By.LINK_TEXT, str(page+1)).send_keys(Keys.ENTER)        
    time.sleep(1)
whole_score_txt1=[]
#리뷰에 해당하는 영화 총점만 추출   
whole_score_txt1.append(movie_tscore[1::2])

#총 리뷰 개수만 추출
txt3=txt2.replace('총', '').replace('개의 평점이 있습니다.', '')
print("<총",txt3,"건 수집완료 되었습니다.>")
print()
print("<NAVER 리뷰 크롤링이 완료되었습니다.>")
print()
print("----------------------------------------------------------------")
driver.close()

# csv 파일로 저장
#저장경로 확인하기
f_dir=os.getcwd()
print(f_dir,"\n위 경로에 파일을 저장합니다.")

whole_score_txt=whole_score_txt1[0]  #1차원 리스트로 수정

print(whole_score_txt1)
print(movie_name_txt)

# #csv 파일 생성
# naver_review=pd.DataFrame()
# naver_review["리뷰번호"]=movie_num_txt
# naver_review["영화제목"]=movie_name_txt
# naver_review["리뷰내용"]=review_txt
# naver_review["리뷰별점"]=list_netizen_score_txt
# naver_review["영화총점"]=whole_score_txt
# naver_review["리뷰작성일자"]=date_txt

# #파일 저장
# naver_review.to_csv("naver_review.csv", encoding='utf-8-sig', index=False)
