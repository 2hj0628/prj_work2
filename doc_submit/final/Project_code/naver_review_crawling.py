'''
***실행 프로세스***
0. 프로젝트 구동을 위한 모듈 임포트 : line 12 - line 47

1. 크롬 디버거 구동 : line 52 - line 71

2. 데이터 수집 : line 73 - line 194

3. 데이터 저장 : line 197 - line 221
'''

# 프로젝트 구동을 위한 필수 모듈 임포트 및 설치
import subprocess    #새로운 프로세스를 생성
import sys       #파이썬이 제공하는 변수와 함수를 직접 제어
import warnings  # warning 출력 제어

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC 
    from bs4 import BeautifulSoup
    import chromedriver_autoinstaller
    import pandas as pd
    import xlwt
except: #모듈이 설치되어있지 않을 경우 
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'selenium'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'bs4'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pandas'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'xlwt'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'chromedriver_autoinstaller'])
finally:
    #크롤링 구동을 위한 모듈  
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup   #데이터 추출(파싱)
    import selenium    # 웹 브라우저와 연결
    import chromedriver_autoinstaller   #크롬드라이버 자동 설치
    import time     #시간제어
    #파일 저장을 위한 모듈
    import pandas as pd   #데이터 분석, 데이터 객체화
    import xlwt   #엑셀파일 생성 및 작성
    import os    #환경변수나 디렉토리, 파일 등의 OS자원 제어

# 콘솔에 warning 문구 출력 안하기
warnings.filterwarnings('ignore')

#크롤링 페이지 연결을 위한 디버거 크롬 구동------------------------------------
##디버거 크롬
datadir=os.getcwd()+r'\chrometemp'    
try:
    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="'+datadir+r'"') 
except:
    subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="'+datadir+r'"')
option=Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

##크롬 버전확인하여 chromedriver 설치하고 구동
chrome_ver=chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver=webdriver.Chrome(service=Service(f'./{chrome_ver}/chromedriver.exe'), options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver=webdriver.Chrome(service=Service(f'./{chrome_ver}/chromedriver.exe'), options=option)
    print(chrome_ver,"chrometemp 폴더 생성 후 Chromedriver를 설치하였습니다.")
#html페이지소스 전체로딩후 연결, 최대10초 대기
driver.implicitly_wait(10)

#데이터 수집------------------------------------------------------------------------------------------------------------
#크롤링할 페이지 연결
url1="https://movie.naver.com/movie/point/af/list.naver"
driver.get(url1)
print("----------------------------------------------------------------")
print("< NAVER 영화리뷰 크롤링을 시작합니다.>")
print("\n--------'네티즌 평점:네이버영화' 페이지에 접속합니다--------")
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
time.sleep(1)
full_html=driver.page_source    
soup=BeautifulSoup(full_html,'html.parser')

##전체 게시물 수 : txt2
content_num=soup.find_all('div','h5_right_txt')
for num1 in content_num:
    txt2=num1.get_text().strip()
print(txt2)

print("\n데이터를 수집하고 있습니다.\n")

#데이터 추출
for page in range(1,3):  #크롤링 할 페이지 수 설정
        
    full_html=driver.page_source    
    soup=BeautifulSoup(full_html,'html.parser')

    ##리뷰 번호  : movie_num_txt[]
    movie_num=soup.find_all('td','ac num')
    for review_num in movie_num:
        txt=review_num.get_text().strip()
        movie_num_txt.append(txt)
        # if txt not in movie_num_txt:       # 리뷰가 계속 업데이트 되므로, 만약 리뷰번호가 이미 있다면 크롤링 하지 않음.
        #     movie_num_txt.append(txt)
        # else : 
        #     continue

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
            time.sleep(0.5)
            #영화 총점 조회 페이지로 넘어가기
            # movie_btn=driver.find_element(By.LINK_TEXT,name)
            movie_btn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT,name)))  # 인식못할시 20초간 대기,인식하면 바로 실행
            movie_btn.click()
            time.sleep(1)

            #바뀐 페이지 읽어오기
            movie_html=driver.page_source    
            movie_soup=BeautifulSoup(movie_html,'html.parser')
            score_movie=movie_soup.find('tbody').find('strong')
            movie_tscore.append(name)    #영화제목
            time.sleep(1)
            movie_tscore.append(score_movie.get_text().replace('/','').replace('10','').strip())   #해당영화의 총 별점

            time.sleep(0.5)
            driver.back()
            time.sleep(0.5)
        
    ##페이지 넘기기
    driver.find_element(By.LINK_TEXT, str(page+1)).send_keys(Keys.ENTER)        
    time.sleep(1)


#리뷰에 해당하는 영화 총점만 추출   
whole_score_txt.append(movie_tscore[1::2])

#총 리뷰 개수만 추출
txt3=txt2.replace('총', '').replace('개의 평점이 있습니다.', '')

print("<총",int(page)*10,"건 수집완료 되었습니다.>")   #실제 수집한 데이터 수
print()
print("<NAVER 리뷰 크롤링이 완료되었습니다.>")
print()
print("----------------------------------------------------------------")
driver.close()

# print(movie_num_txt)
# print(movie_name_txt)
# print(review_txt)
# print(list_netizen_score_txt)
# print(whole_score_txt)
# print(date_txt)

# csv 파일로 저장------------------------------------------------------------------------------------------------------------
#저장경로 확인하기
os.path.exists('./result_data') 
if not os.path.exists('./result_data'):
    os.mkdir('./result_data')
os.chdir('./result_data')
f_dir=os.getcwd()
print(f_dir,"\n위 경로에 파일을 저장합니다.")

del whole_score_txt[0][0:10]  #페이지 이동시 첫페이지 중복크롤링되므로 del
whole_score_txt=whole_score_txt[0]  #1차원 리스트로 수정

#csv 파일 생성
naver_review=pd.DataFrame()
naver_review["리뷰번호"]=movie_num_txt
naver_review["영화제목"]=movie_name_txt
naver_review["리뷰내용"]=review_txt
naver_review["리뷰별점"]=list_netizen_score_txt
naver_review["영화총점"]=whole_score_txt
naver_review["리뷰작성일자"]=date_txt

#파일 저장
naver_review.to_csv("naver_review.csv", encoding='utf-8-sig', index=False)

print("'naver_review.csv' 파일 저장이 완료되었습니다.")