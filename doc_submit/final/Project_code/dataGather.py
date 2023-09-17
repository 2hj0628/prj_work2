'''
***실행 프로세스***
0. 프로젝트 구동을 위한 모듈 임포트 : line 10 ~ line 29
1. DB생성 : line 34 ~ line 40
2. Table생성 : line 42 ~ line 98
3. 네이버 리뷰 테이블 삽입 : line 102 ~ line 127
4. 코비스 영화 테이블 삽입 : line 132 ~ line 160
'''

# 프로젝트 구동을 위한 필수 모듈 임포트 및 설치
import subprocess
import sys
import warnings  # warning 출력 제어

try:
    import requests
    from bs4 import BeautifulSoup
    import pymysql
    import pandas as pd
except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'requests'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'bs4'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pymysql'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pandas'])
finally:
    import requests
    from bs4 import BeautifulSoup
    import pymysql
    import pandas as pd
    import sqlite3 as sql
    import re
    import csv

# 콘솔에 warning 문구 출력 안하기
warnings.filterwarnings('ignore')

#db생성------------------------------------------------------------------------------------------------------
print()
print('--------------------------------------------------')
print()
print('‘film_innerside’ 데이터베이스 생성')
print()
print('--------------------------------------------------')
print()
conn = pymysql.connect(host='localhost',user='root',password='1234',charset='utf8')  #mysql에 연결(host,user,password,charset 파라미터 지정)
curs=conn.cursor(pymysql.cursors.DictCursor)  #cursor 객체 생성
curs.execute('create database if not exists film_innerside')  #db생성(create db 입력)
curs.execute('use film_innerside')  #db사용(use db 입력)

#네이버리뷰 가더 테이블 생성--------------------------------------------------------------------------------------
print('‘naver_review_gather’ 테이블 생성')
curs.execute('''create table if not exists naver_review_gather(
    gid int auto_increment, 
    gmovie varchar(40) not null, 
    gdate date, 
    greview varchar(1000), 
    gpoint int(2) check(0 <= gpoint and gpoint <= 10), 
    gsumpoint int(2) check(0 <= gsumpoint and gsumpoint <= 10), 
    gnum varchar(10) not null unique, 
    primary key(gid)
)''')

#코비스 가더 테이블 생성-----------------------------------------------------------------------------------------------------
print('‘kobis_movie_gather’ 테이블 생성')
curs.execute('''create table if not exists kobis_movie_gather(
    gid int auto_increment, 
    gmovie varchar(100) not null, 
    gdate date not null, 
    gaudience int(10) not null, 
    ggenre varchar(50), 
    gopendate date, 
    gdirec varchar(500), 
    gactor varchar(500), 
    gmovie_id varchar(100) not null unique,
    primary key(gid)
)''')

#네이버리뷰 스크럽 테이블 생성-------------------------------------------------------------------------------------------------
print('‘naver_review_scrub’ 테이블 생성')
curs.execute('''create table if not exists naver_review_scrub(
    sid int auto_increment, 
    smovie varchar(40) not null, 
    sdate date, 
    sreview varchar(200), 
    spoint int(2) check(0 <= spoint and spoint <= 10), 
    ssumpoint int(2) check(0 <= ssumpoint and ssumpoint <= 10), 
    snum varchar(10) not null unique,
    label	int(1),
    positive int(2) check(0 <= positive and positive <= 10),
    primary key(sid)
)''')

#코비스 스크럽 테이블 생성-----------------------------------------------------------------------------------------------------
print('‘kobis_movie_scrub’ 테이블 생성')
curs.execute('''create table if not exists kobis_movie_scrub(
    sid int auto_increment, 
    smovie varchar(40) not null, 
    sdate date not null, 
    saudience int(10) not null, 
    sgenre varchar(10), 
    sopendate date, 
    sdirec varchar(10), 
    sactor varchar(50), 
    smovie_id varchar(100) not null unique,
    primary key(sid)
)''')



#네이버리뷰 테이블에 넣기-------------------------------------------------------------------------------------------------------------
print()
print('--------------------------------------------------')
print()
print('naver_review.csv')
print('☞ ‘naver_review_gather’ 테이블에 저장')

f_nr=open('./result_data/naver_review.csv','r', encoding='utf8')  #절대경로\\naver_review.csv 읽기모드 utf8로 열기
data=csv.reader(f_nr)  #변수data로 csv읽기
next(data)  #맨 위 컬럼명들(한줄) 넘기기

num=0  #gid를 생성을 위한 num
for row in data:  #csv를 row(한줄씩) 읽기
    try:
        #번호(int)-영화제목-날짜(date)-리뷰내용-리뷰별점(int)-총점(int)-리뷰코드(int)
        num+=1  #gid생성을 위한 num+=1
        row[1]=row[1].replace("'","")  #영화제목에 '(작은 따옴표)가 있으면 sql문법오류 발생으로 제거함

        #naver_review_gather테이블에 다음과 같은 values를 insert함
        #문자열과 date값은 db에 옮길때 문법오류로 인해 '{1}'<-따옴표필요
        query = '''insert INTO naver_review_gather VALUES (
        {0},'{1}','{2}','{3}',{4},{5},{6}
        )'''.format(num,row[1],row[5],row[2],row[3],row[4],row[0])  #gid,gmovie,gdate,greview,gpoint,gsumpoint,gnum
        curs.execute(query)  #insert문 실행
    except:
        pass  #리뷰코드 중복오류시 pass

f_nr.close()  #naver_review.csv 읽기모드 닫기



#코비스 테이블에 넣기----------------------------------------------------------------------------------------------------------------
print()
print('--------------------------------------------------')
print()
print('kobis_movie.csv')
print('kobis_rank.csv')
print('☞ ‘kobis_movie_gather’ 테이블에 저장')

f_kr=open('./result_data/kobis_rank.csv','r', encoding='utf8')  #절대경로\\kobis_rank.csv 읽기모드 UTF8로 열기
k_rank=csv.reader(f_kr)  #변수k_rank로 csv읽기
next(k_rank)  #맨 위 컬럼명들(한줄) 넘기기

f_km=open('./result_data/kobis_movie.csv','r', encoding='utf8')  #절대경로\\kobis_movie.csv 읽기모드 UTF8로 열기
k_movie=csv.reader(f_km)  #변수k_movie로 csv읽기
next(k_movie)  #맨 위 컬럼명들(한줄) 넘기기

num=0  #gid를 생성을 위한 num(위와 같음)
for row1,row2 in zip(k_rank,k_movie):  #csv가 2개이므로 각각의 csv를 row1,row2가 한줄씩 읽음
    try:
        num+=1  #gid생성을 위한 num+=1
        # 번호(int)-영화제목-날짜(date)-관객(int)-장르-개봉일(date)-감독-배우-코드
        row2[0]=row2[0].replace("'","")  #영화제목에 '(작은 따옴표)가 있으면 sql문법오류 발생으로 제거함

        #문자열과 date값은 db에 옮길때 문법오류로 인해 '{1}'<-따옴표필요
        #gmovie_id는 숫자지만 테이블 생성시 문자열로 지정했으므로 '{8}'<-따옴표필요
        query = '''insert INTO kobis_movie_gather VALUES (
        {0}, '{1}', '{2}', {3},'{4}','{5}','{6}','{7}','{8}'
        )'''.format(num,row2[0],row1[1],row1[3],row2[2],row1[4],row2[3],row2[4],row2[1])  #gid,gmovie,gdate,gaudience,ggenre,gopendate,gdirec,gactor,gmovie_id
        curs.execute(query)  #insert문 실행
    except:
        pass  #리뷰코드 중복오류시 pass
    
f_kr.close()  #kobis_rank.csv 읽기모드 닫기
f_km.close()  #kobis_movie.csv 읽기모드 닫기

conn.commit()  #저장
conn.close()  #닫기

print()
print('--------------------------------------------------')
print()
print('DB저장을 완료하였습니다.')
print()
print('--------------------------------------------------')
print()