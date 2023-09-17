
import time
from dataScrub import reviewPre
from dataScrub import kobisPre
from dataScrub import wordIntVector
from dataScrub import modelFit
from dataScrub import positiveIdx
# from dataScrub import kobisLoad
# from dataScrub import reviewLoad


print("\n\n＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿")
print(" ####   NAVER 영화 리뷰 : 데이터 전처리 및 감성분석   ####")
print("￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣")
print("                                               ver1.0")


'''
# 변수 명명규칙
tab_ 로 시작하면, 테이블명을 의미
~cols 로 끝나면, 컬럼명을 의미
rev_~ 로 시작하면, 네이버 영화리뷰 관련을 의미
kobis_~ 로 시작하면, KOBIS 영화관 입장권 관련을 의미

'''

## 네이버 영화 리뷰 데이터를 naver_review_gather 테이블에서 로딩
## 리뷰 전처리한거 naver_review_scrub 테이블에 저장
tab_ngather='naver_review_gather'
tab_nscrub='naver_review_scrub'
rev_gcols=['gid','gmovie','gdate','greview','gpoint','gsumpoint','gnum']
rev_scols=['smovie','sdate','sreview','spoint','ssumpoint','snum','label']
rev_scols_posi=['snum','positive']  #예측한 긍정지수를 저장시 사용될 컬럼명

## KOBIS 영화관 입장권 데이터를 kobis_movie_gather 테이블에서 로딩
## 전처리한거 kobis_movie_scrub 테이블에 저장
tab_kgather='kobis_movie_gather'
tab_kscrub='kobis_movie_scrub'
kobis_gcols=['gid', 'gmovie', 'gdate', 'gaudience', 'ggenre', 'gopendate', 'gdirec', 'gactor', 'gmovie_id']
kobis_scols=['smovie', 'sdate', 'saudience', ' sgenre', 'sopendate', 'sdirec', 'sactor', 'smovie_id']


for i in range(1):
    ## 리뷰 데이터 전처리
    print('\n*** [ STEP 1 ] 네이버 영화 리뷰 데이터 전처리  : 신규 수집 데이터 ***')
    key=input('STEP 1을 진행하시겠습니까? (진행:Y, 종료:0)  ')
    if key=='y' or key=='Y':
        try:
            refine_df=reviewPre(tab_ngather,tab_nscrub,rev_gcols,rev_scols)
            # progress=True        
            time.sleep(1)
        except UnboundLocalError:
            # progress=False
            print('>>>> None... 신규 수집 데이터가 없습니다.')
    elif key=='0':        
        break
    else:
        print('STEP 1 을 진행하지 않습니다.')

    ## 리뷰 토큰의 정수 시퀀스, 벡터 변환
    ## 토근화 한거 naver_review_scrub 테이블에 저장
    print('\n\n*** [ STEP 2 ] 단어 토큰화 및 불용어 삭제  ***')
    key=input('STEP 2를 진행하시겠습니까? (진행:Y, 종료:0)  ')
    if key=='y' or key=='Y':
        token_df, X_train=wordIntVector('sreview','label','snum',tab_nscrub)       
        token_df.to_csv('naver_review_scrub.csv', encoding="UTF-8-sig", index=False)
        time.sleep(1)
            

    ## 모델 검증 훈련
        print('\n\n*** [ STEP 3 ] 모델 훈련 및 검증  ***')
        model, X_train=modelFit(X_train, token_df['label'])

    ## 긍정지수 산출
    # 산출한 긍정지수 DB에 저장
    # table: naver_review_scrub
        positive, review_num=positiveIdx(model,X_train,token_df,rev_scols_posi,tab_nscrub)
        time.sleep(4)
    
    elif key=='0':        
        break
    else:
        print('STEP 2 / STEP 3 을 진행하지 않습니다.')


    print("\n\n＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿")
    print(" ####    KOBIS 영화관 입장권 통합 : 데이터 전처리   ####")
    print("￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣")

    print('\n\n*** [ STEP 1 ] 영화관 입장권 수집 데이터 전처리  ***')
    key=input('STEP 1을 진행하시겠습니까? (진행:Y, 종료:0)  ')
    if key=='y' or key=='Y':
    # 영화관 입장권 데이터 전처리     
        refine_df=kobisPre(tab_kgather,tab_kscrub,kobis_gcols,kobis_scols)
    elif key=='0':        
        break
    else:
        print('STEP 1 을 진행하지 않습니다.')


      

print('\n\n\n\n')




