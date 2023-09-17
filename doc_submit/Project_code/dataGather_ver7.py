import requests
from bs4 import BeautifulSoup
import sqlite3 as sql
import pymysql
import re


#네이버 리뷰 리스트-----------------------------------------------------------------------------
gid_n=[]
gdate_n=[]
gpoint=[]
gsumpoint=[]

for i in range(len(movie_num_txt)):  #번호
    gid_n.append(i+1)

for i in date_txt:  #날짜
    gdate_n.append('20'+i[-8:].replace('.','-'))

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
    gopendate.append(rank_list[i][3])  #개봉일
    gdate1.append(rank_list[i][0])
    gdate2=re.findall('\d+',gdate1[i])
    gdate_k.append('-'.join(gdate2))  #날짜

for i in range(len(movie_info_cont)):
    gmovie_id.append(movie_info_cont[i][1])  #코드(식별코드)
    ggenre1.append(movie_info_cont[i][4].split('|'))
    
for i in range(len(ggenre1)):
    ggenre.append(ggenre1[i][2])  #장르

for i in movie_staff:
    gdirec.append(str(list(i.values())[0])[1:-1].replace("'",""))  #감독
    gactor.append(str(list(i.values())[1])[1:-1].replace("'",""))  #주연배우


#db생성------------------------------------------------------------------------------------------------------
conn = pymysql.connect(host='localhost',user='root',password='1234',charset='utf8')
curs=conn.cursor(pymysql.cursors.DictCursor)
curs.execute('create database film_innerside123')
curs.execute('use film_innerside123')

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
    sql_n='INSERT INTO naver_review_gather1 VALUES(%s,%s,%s,%s,%s,%s,%s)'
    val_n=(a,b,c,d,e,f,g)
    curs.execute(sql_n,val_n)

#코비스 테이블에 넣기
for a,b,c,d,e,f,g,h,i in zip(gid_k,gmovie_k,gdate_k,gaudience,ggenre,gopendate,gdirec,gactor,gmovie_id):
    sql_k='INSERT INTO kobis_movie_gather1 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    val_k=(a,b,c,d,e,f,g,h,i)
    curs.execute(sql_k,val_k)

conn.commit()
conn.close()