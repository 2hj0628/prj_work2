=================================================================================
[ 프로젝트 파일 구조 ]
Project_code > 
	scrub_main.py	- 네이버 영화 리뷰 수집데이터 전처리 및 감성분석, 영화관 입장권 데이터 전처리	** 실행파일
	dataGather.py 	- DB 저장								** 실행파일
	naver_movie_review.py	- 네이버 영화 리뷰 크롤러					** 실행파일
	kobis_crawling_vscode.py	- KOBIS 영화관 입장권 크롤러					** 실행파일
	dataScrub.py	- 데이터 전처리 및 감성분석 실행 함수
	dbProc.py		- db 실행 함수
	DB_ver0.1.sql	- db 생성 구문
Project_code > data
	stopwords.txt	- 불용어
=================================================================================


[ 실행전 환경 설정 ]

################ Visual Studio Code 확장팩 설치
- python
- python for VSCode
- Python Extension Pack
- Code Runner

################ Visual Studio Code 확장팩 - Code Runner 설정변경
1. 왼쪽의 플러그인 창에서 code runner를 검색해서 톱니바튀 버튼을 누른 뒤 Extension Settings ( 확장설정 ) 를 선택
2. 중간 쯤에 있는 Code-runner : Run In Terminal 을 체크


################  java JSK 설치
https://www.oracle.com/java/technologies/downloads/#jdk19-windows
1. 다운로드 : Java 19 > Windows > x64 Installer
2. 시스템 환경 변수 설정
   내컴퓨터 - 우클릭 속성 - 고급 시스템 설정 - 고급 - 환경 변수
   User에 대한 사용자 변수 -  Path  - 편집하여 추가
%JAVA_HOME%bin

3. 시스템 변수 - 새로만들기하여 추가
변수이름 : JAVA_HOME
변수값 : C:\Program Files\Java\jdk-19


################  mySQL 설치
http://dev.mysql.com/downloads/
1. MySQL설치파일 다운로드 : mysql-installer-community-8.0.30.0.msi
2. 시스템 환경 변수 설정
   내컴퓨터 - 우클릭 속성 - 고급 시스템 설정 - 고급 - 환경 변수
   User에 대한 사용자 변수 -  Path  - 편집하여 추가
C:\Program Files\MySQL\MySQL Server 8.0\bin


################ CUDA 최신 버전 다운로드
https://developer.nvidia.com/cuda-toolkit-archive

1. Download Lastest CUDA Toolkit 다운로드 후 설치 진행
2. 시스템 환경 변수 설정
내컴퓨터 - 우클릭 속성 - 고급 시스템 설정 - 고급 - 환경 변수
시스템 변수에 Path 편집하여 추가
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\bin
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\libnvvp


################ Visual Studio Code 구동

1. 인터프리터 설정
(비쥬얼스튜디오) -> ctrl+shift+P -> Python 3.10.6('venv':venv) 선택

2. 폴더 열기
Project_code







