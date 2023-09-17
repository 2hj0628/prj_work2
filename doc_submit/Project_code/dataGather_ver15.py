import requests
from bs4 import BeautifulSoup
import sqlite3 as sql
import pymysql
import re
import pandas as pd
import csv

#db생성------------------------------------------------------------------------------------------------------
conn = pymysql.connect(host='localhost',user='root',password='1234',charset='utf8')
curs=conn.cursor(pymysql.cursors.DictCursor)
curs.execute('create database film_innerside')
curs.execute('use film_innerside')

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

num=0
#네이버리뷰 테이블에 넣기
f=open('naver_review.csv','r', encoding='UTF8')
data=csv.reader(f)
next(data)

for row in data:
    try:
        #번호(int)-영화제목-날짜(date)-리뷰내용-리뷰별점(int)-총점(int)-리뷰코드(int)
        num+=1
        row[1]=row[1].replace("'","")
        row[2]=row[2].replace("[","").replace("]","")
        row[5]='20'+row[5].replace('.','-')
        query = '''insert INTO naver_review_gather VALUES (
        {0},'{1}','{2}',{3},{4},{5},{6}
        )'''.format(num,row[1],row[5],row[2],row[3],row[4],row[0])
        curs.execute(query)
    except:
        pass  #리뷰코드 중복오류시 pass

f.close()

#코비스 테이블에 넣기
f1=open('kobis_rank.csv','rt')
k_rank=csv.reader(f1)
next(k_rank)

f2=open('kobis_movie.csv','rt')
k_movie=csv.reader(f2)
next(k_movie)

num=0
for row1,row2 in zip(k_rank,k_movie):
    try:
        num+=1
        # 번호(int)-영화제목-날짜(date)-관객(int)-장르-개봉일(date)-감독-배우-코드
        row2[0]=row2[0].replace("'","")
        query = '''insert INTO kobis_movie_gather VALUES (
        {0}, '{1}', '{2}', {3},'{4}','{5}','{6}','{7}','{8}'
        )'''.format(num,row2[0],row1[1],row1[3],row2[2],row1[4],row2[3],row2[4],row2[1])
        curs.execute(query)
    except:
        pass  #리뷰코드 중복오류시 pass
    
f1.close()
f2.close()

conn.commit()
conn.close()