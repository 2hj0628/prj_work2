-- film_innerside 데이터베이스 생성하기
create database film_innerside;

-- 데이터베이스 목록 조회
show databases;

-- film_innerside 데이터베이스 접근
use `film_innerside`;

-- 네이버 영화 리뷰 수집 테이블 생성 
create table `naver_review_gather`(
    gid			INT 		AUTO_INCREMENT,
    gmovie		VARCHAR(40)	Not Null,
    gdate		DATE,
    greview		VARCHAR(1100),
    gpoint		INT(2)	CHECK(gpoint >= 0 AND gpoint <= 10),
    gsumpoint		FLOAT(5),
    gnum		VARCHAR(10)	Not Null	UNIQUE,
    primary key(gid)
);

-- 네이버 영화 리뷰 수집 테이블 구조 보기
DESC `naver_review_gather`;

-- KOBIS영화관입장권 수집 테이블 생성
create table `kobis_movie_gather`(
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
);

-- KOBIS영화관입장권 수집 테이블 구조 보기
DESC `kobis_movie_gather`;

-- 네이버 영화 리뷰 정제 테이블 생성 
CREATE TABLE `naver_review_scrub`(
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
);

-- 네이버 영화 리뷰 정제  테이블 구조 보기
DESC `naver_review_scrub`;

-- KOBIS영화관입장권 정제 테이블 생성
CREATE TABLE `kobis_movie_scrub`(
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
);

-- KOBIS영화관입장권 정제 테이블 구조 보기
DESC `kobis_movie_scrub`;

-- 테이블 목록 조회하기
show tables;