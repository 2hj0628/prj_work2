import subprocess
import sys

try:
    import requests
    from bs4 import BeautifulSoup
    import sqlite3 as sql
    import pymysql
    import pandas as pd
except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'requests'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'bs4'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'sqlite3'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pymysql'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pandas'])
    
import requests
from bs4 import BeautifulSoup
import sqlite3 as sql
import pymysql
import re
import pandas as pd
import csv  


#db생성------------------------------------------------------------------------------------------------------
conn = pymysql.connect(host='localhost',user='root',password='1234',charset='utf8')  #mysql에 연결(host,user,password,charset 파라미터 지정)
curs=conn.cursor(pymysql.cursors.DictCursor)  #cursor 객체 생성
curs.execute('create database film_innerside')  #db생성(create db 입력)
curs.execute('use film_innerside')  #db사용(use db 입력)



#네이버리뷰 가더 테이블 생성--------------------------------------------------------------------------------------
curs.execute('''create table `naver_review_gather`(
    gid			INT 		AUTO_INCREMENT,
    gmovie		VARCHAR(40)	Not Null,
    gdate		DATE,
    greview		VARCHAR(1100),
    gpoint		INT(2)	CHECK(gpoint >= 0 AND gpoint <= 10),
    gsumpoint		FLOAT(5),
    gnum		VARCHAR(10)	Not Null	UNIQUE,
    primary key(gid)
)''')

#코비스 가더 테이블 생성-----------------------------------------------------------------------------------------------------
curs.execute('''create table `kobis_movie_gather`(
    gid			INT 	        AUTO_INCREMENT,
    gmovie		VARCHAR(40)	Not Null,
    gdate		DATE		Not Null,
    gaudience	        INT(10)		Not Null,
    ggenre		VARCHAR(30),
    gopendate	        DATE,
    gdirec		VARCHAR(30),
    gactor		VARCHAR(600),
    gmovie_id	        VARCHAR(110)	Not Null	UNIQUE,
    primary key(gid)
)''')

#네이버리뷰 스크럽 테이블 생성-------------------------------------------------------------------------------------------------
curs.execute('''CREATE TABLE `naver_review_scrub`(
    sid		INT		auto_increment,
    smovie	VARCHAR(40),		
    sdate	DATE,				
    sreview	VARCHAR(1100),			
    spoint	INT(2)	CHECK(spoint >= 0 AND spoint <= 10),
    ssumpoint	FLOAT(5),
    snum	VARCHAR(10)	not null	UNIQUE,
    label	INT(1),
    positive	FLOAT(20),
    primary key(sid)
)''')

#코비스 스크럽 테이블 생성-----------------------------------------------------------------------------------------------------
curs.execute('''CREATE TABLE `kobis_movie_scrub`(
    sid		INT		auto_increment,
    smovie	VARCHAR(40)	not null,
    sdate	DATE		not null,
    saudience	INT(10)		not null,
    sgenre	VARCHAR(30),		
    sopendate	DATE,			
    sdirec	VARCHAR(30),		
    sactor	VARCHAR(600),		
    smovie_id	VARCHAR(110)	not null	UNIQUE,	
    primary key(sid)
)''')



#네이버리뷰 테이블에 넣기-------------------------------------------------------------------------------------------------------------
f=open('D:\\prj_work2\\doc_submit\\Project_code\\naver_review.csv','r', encoding='UTF8')  #절대경로\\naver_review.csv 읽기모드 utf8로 열기
data=csv.reader(f)  #변수data로 csv읽기
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

f.close()  #naver_review.csv 읽기모드 닫기



#코비스 테이블에 넣기----------------------------------------------------------------------------------------------------------------
f1=open('D:\\prj_work2\\doc_submit\\Project_code\\kobis_rank.csv','r', encoding='UTF8')  #절대경로\\kobis_rank.csv 읽기모드 UTF8로 열기
k_rank=csv.reader(f1)  #변수k_rank로 csv읽기
next(k_rank)  #맨 위 컬럼명들(한줄) 넘기기

f2=open('D:\\prj_work2\\doc_submit\\Project_code\\kobis_movie.csv','r', encoding='UTF8')  #절대경로\\kobis_movie.csv 읽기모드 UTF8로 열기
k_movie=csv.reader(f2)  #변수k_movie로 csv읽기
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
    
f1.close()  #kobis_rank.csv 읽기모드 닫기
f2.close()  #kobis_movie.csv 읽기모드 닫기

conn.commit()  #저장
conn.close()  #닫기



