import requests
from bs4 import BeautifulSoup
import sqlite3 as sql
import pymysql
import re
import pandas as pd

#네이버 리뷰 리스트-----------------------------------------------------------------------------
gid_n=[]
gdate_n=[]
gpoint=[]
gsumpoint=[]
gnum=[]

for i in range(len(movie_num_txt)):  #번호
    gid_n.append(i+1)

for i in movie_num_txt:  
        gdate_n.append('20'+i.replace('.','-'))  #날짜

for i in list_netizen_score_txt:  #별점
    gpoint.append(int(i))

for i in whole_score_txt:  #총점
    gsumpoint.append(int(i))

gmovie_n=movie_name_txt  #영화제목
greview=review_txt  #리뷰
gnum=movie_num_txt  #리뷰번호(식별코드)

#코비스 리스트---------------------------------------------------------------------------------------------
gid_k=[]
gmovie_k=[]
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
    gmovie_id.append(movie_info_cont[i][1])  #코드(식별코드)
    ggenre1.append(movie_info_cont[i][4].split('|'))
    
for i in range(len(ggenre1)):
    ggenre.append(ggenre1[i][2])  #장르

for i in movie_staff:
    gdirec.append(str(list(i.values())[0])[1:-1].replace("'",""))  #감독
    gactor.append(str(list(i.values())[1])[1:-1].replace("'",""))  #주연배우


#코비스 csv 생성---------------------------------------------------------------------------------------------
kobis=pd.DataFrame()
kobis['번호']=gid_k
kobis['영화제목']=gmovie_k
kobis['관객수']=gaudience
kobis['날짜']=gdate_k
kobis['개봉일']=gopendate
kobis['코드']=gmovie_id
kobis['장르']=ggenre
kobis['감독']=gdirec
kobis['주연배우']=gactor

kobis.to_csv('C:\kobis.csv',encoding='utf-8-sig',index=False)


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

#네이버리뷰 테이블에 넣기
for a,b,c,d,e,f,g in zip(gid_n,gmovie_n,gdate_n,greview,gpoint,gsumpoint,gnum):
    sql_n='INSERT INTO naver_review_gather VALUES(%s,%s,%s,%s,%s,%s,%s)'
    val_n=(a,b,c,d,e,f,g)
    curs.execute(sql_n,val_n)

#코비스 테이블에 넣기
for a,b,c,d,e,f,g,h,i in zip(gid_k,gmovie_k,gdate_k,gaudience,ggenre,gopendate,gdirec,gactor,gmovie_id):
    sql_k='INSERT INTO kobis_movie_gather VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    val_k=(a,b,c,d,e,f,g,h,i)
    curs.execute(sql_k,val_k)

conn.commit()
conn.close()