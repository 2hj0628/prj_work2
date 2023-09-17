import requests
from bs4 import BeautifulSoup
import sqlite3 as sql
import pymysql
import re

#네이버 리뷰 리스트
gid_n=[]
gdate_n=[]

for i in range(len(movie_num_txt)):  #번호
    gid_n.append(i+1)

for i in date_txt:  #날짜
    gdate_n.append('20'+i[-8:].replace('.','-'))

gmovie_n=movie_name_txt  #영화제목
greview=review_txt  #리뷰
gpoint=int(list_netizen_score_txt)  #별점
gsumpoint=int(whole_score_txt)  #총점
gnum=movie_num_txt  #리뷰번호(식별코드)

#코비스 리스트
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
    gaudience.append(rank_list[i][8])  #관객수
    gopendate.append(rank_list[i][3])  #개봉일
    gmovie_id.append(movie_info_cont[i][1])  #코드(식별코드)
    gdate1.append(rank_list[i][0])
    gdate2=re.findall('\d+',gdate1[i])
    gdate_k.append('-'.join(gdate2))  #날짜
    ggenre1.apppend(movie_info_cont[i][4].split('|'))
    ggenre.append(ggenre1[i][2])  #장르
    
new_movie_staff=list(movie_staff.values())
for i in new_movie_staff:
    if new_movie_staff.index(i)%2==0:
        gdirec.append(i)  #감독
    else:
        gactor.append(i)  #주연배우

#db생성
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