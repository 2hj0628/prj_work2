import subprocess
import sys

try:
    import openpyxl
    import pandas as pd
    import numpy as np
    import matplotlib
    import tqdm
    import konlpy
    import tensorflow    
except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'openpyxl'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pandas'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'numpy'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'matplotlib'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'tqdm'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'konlpy'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'tensorflow'])     
finally:
    from konlpy.tag import Okt
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow import keras
    from tensorflow.keras import layers
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from tqdm import tqdm

    import time
    import os    

    from dbProc import exeSql
    from dbProc import insQry

# CUDA dll 위치지정
os.add_dll_directory('C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.8\\libnvvp')

### 데이터 불러오기
"""
파라미터 : url,data type
리턴값 : DataFrame 객체
"""
def dataRead(url,type):
    if type=='xlsx':
        data=pd.read_excel(url)
    elif type=='csv':
        data=pd.read_csv(url,sep=',')
    elif type=='txt':
        data=pd.read_csv(url,sep='\t')
        # data=pd.read_table(url)
    return data

## 데이터를 데이터프레임에 담기
"""
파라미터 : data,columns
리턴값 : DataFrame 객체
"""
def dfAppend(data,_cols):
    df=pd.DataFrame(columns=_cols)
    i=0
    for dic in tqdm(data):
        tail=pd.DataFrame(dic,index=[i])
        df=pd.concat([df,tail],axis=0)
        i+=1
    return df

### label 라벨(긍정,부정) 추가
# 리뷰별점(1~10)을 3범주로 설정하여 긍정/부정 레이블 설정
# 긍정 리뷰 (8~10점) : label=1
# 부정 리뷰 (0~4점) : label=0
# 평균 리뷰 (5~7점) : label=2
"""
파라미터 : gpoint
리턴값 : 0,1,2 중 해당하는 값
"""
def reLabel(gpoint):
    label=[]
    # for point in df['gpoint']:
    for point in gpoint:
        if point>=0 and point<5:
            label.append(0)
        elif point>=8 and point<=10:
            label.append(1)
        else:
            label.append(2)
    return label

## 날짜 DATE형식을 텍스트 처리하기
def toText(gather,idx):
    for i in range(len(gather)):
        gdate=gather[i][idx]
        # gdate=str(gdate)
        gather[i][idx]=str(gdate)  
    return gather

### 토큰화
"""
파라미터 : greview
리턴값 : 토큰화한 리스트
"""
def tokenWords(greview):
    # 불용어    
    url='.\\data\\stopwords.txt'    
    stopwords=dataRead(url,'txt')
        
    # 형태소 분석기
    okt=Okt()
    
    # 토큰화 및 불용어 제거
    X_data=[]    
    for sen in tqdm(greview):
        tokenized_sen = okt.morphs(sen,stem=True)
        stopwords_removed_sen=[word for word in tokenized_sen if not word in stopwords]
        X_data.append(stopwords_removed_sen)

    return X_data


### 네이버 영화 리뷰 데이터 전처리
"""
파라미터 : tables, columns
리턴값 : DataFrame 객체
"""
def reviewPre(tab_gather,tab_scrub,gcols,scols):    
    # 리뷰 데이터 불러오기
    print('\n>>>> Connecting... 데이터베이스 접속')        
    # qry='select * from %s;' % (tab_gather)
    qry="SELECT * FROM %s WHERE NOT EXISTS (SELECT * FROM %s WHERE %s.%s=%s.%s);" % (tab_gather,tab_scrub,tab_gather,'gnum',tab_scrub,'snum')        
    rev_gather=exeSql(qry,'film_innerside',1)
    
    #날짜 DATE형식을 텍스트 처리하기
    rev_gather=toText(rev_gather,'gdate')   
    

    # 데이터프레임에 담기
    print('\n>>>> Loading... 네이버 영화 리뷰 데이터')
    df=dfAppend(rev_gather,gcols)
    

    # label 라벨(긍정,부정) 추가
    df['label']=reLabel(df['gpoint'])
    print('>>>> Refinementing... 리뷰 라벨 추가')

    
    # 한글과 공백을 제외하고 제거
    df['gmovie']=df['gmovie'].str.replace('^ +|\'|;',' ',regex=True)    
    df['greview']=df['greview'].str.replace('[^ ㄱ-ㅎㅏ-ㅣ가-힣]','',regex=True)
    print('>>>> Refinementing... 한글 정제')


    # white space 데이터를 NaN으로 변경
    df['greview']=df['greview'].str.replace('^ +','',regex=True)    
    df.replace('', np.nan, inplace=True)
    print('>>>> Refinementing... 여백 정제')

    # NaN 값 제거
    df=df.dropna(how='any', axis=0)
    print('>>>> Refinementing... 결측치 정제')


    # 중복값 제거
    df.drop_duplicates('greview', inplace=True)
    print('>>>> Refinementing... 중복 정제')

    time.sleep(0.5)
    

    # 토큰화    
    print('\n>>>> Tokenizing... 단어 토큰화')
    print('>>>> Tokenizing... 불용어 정제')
    df['greview']=tokenWords(df['greview'])           
    time.sleep(1)
        
    print('\n>>>> Uploading... DB 저장')    
    insQry(tab_scrub,scols,df,1)
    
    return df


# 단어 빈도 확인
"""
파라미터 : tokennizer 객체
리턴값 : vocab_size -단어집합크기
"""
def wordCnt(tokenizer):
    threshold=3     #기준값
    total_cnt=len(tokenizer.word_index) #단어의 수
    rare_cnt=0      #빈도수가 기준값보다 작은 단어의 카운트
    total_freq=0    #훈련 데이터의 전체 단어 빈도수 총 합
    rare_freq=0     #빈도수가 기분값보다 작은 단어의 빈도수 총 합

    for key, vlaue in tokenizer.word_counts.items():
        total_freq=total_freq+vlaue

        # 기준값보다 작으면
        if (vlaue < threshold):
            rare_cnt=rare_cnt+1
            rare_freq=rare_freq+vlaue

    vocab_size=total_cnt-rare_cnt+1
    print('\n┌──────────────────────────────────────────────────┐')        
    print('│ [*] 단어 집합(vocabulary)의 총 크기 : %d     │' % total_cnt)
    print('│ [*] 빈도가 %s번 이하인 단어의 수: %s           │' % (threshold-1,rare_cnt))    
    print('│ [*] 전체에서 희귀 단어의 빈도 비율 : %.2f%s       │' % (rare_freq/total_freq*100,'%'))
    print('│ [*] 사용할 단어 집합의 크기 : %d               │' % vocab_size)
    print('└──────────────────────────────────────────────────┘')

    return vocab_size


## 리뷰 토큰의 정수 시퀀스, 벡터 변환
"""
파라미터 : review, label, review num, table
리턴값 : dataframe 객체, review 백터
"""
def wordIntVector(review,label,num,tab_scrub):    
    ## 데이터 불러오기
    print('\n>>>> Connecting... 데이터베이스 접속')    
    qry='select %s,%s,%s from %s;' % (review,label,num,tab_scrub)
    rev_scrub=exeSql(qry,'film_innerside',1)
    
    # 데이터프레임에 담기
    print('\n>>>> Loading... 네이버 영화 리뷰 데이터')
    df=dfAppend(rev_scrub,[review,label,num])
    
    # 평균리뷰 삭제
    df['label'].replace(2, '', inplace=True)
    df['label'].replace('', np.nan, inplace=True)
    df=df.dropna(how='any', axis=0)
    df=df.reset_index()
    
    # 리뷰 X_train에 담기        
    X_train=df[review]     

    # 리뷰 토큰의 단어집합
    tokenizer=Tokenizer()
    tokenizer.fit_on_texts(X_train)
    print('\n>>>> Vocabulary... 단어 집합화')
    
    # 등장빈도가 1인 단어는 단어집합에서 제외
    vocab_size=wordCnt(tokenizer)
    tokenizer=Tokenizer(vocab_size)
    tokenizer.fit_on_texts(X_train)
    df[review]=X_train
    time.sleep(3)
    print('\n>>>> Vocabulary... 낮은 빈도 단어 정제')
    
    # 단어들을 숫자 시퀀스의 형태로 변환
    X_train=tokenizer.texts_to_sequences(X_train)
    print('>>>> Integer Encoding... 단어의 정수 시퀀스 정제')      

    # 빈값제거
    print('>>>> Vocabulary... 낮은 빈도 단어의 관련 데이터 정제')    
    drop_idx=[idx for idx, sen in enumerate(X_train) if len(sen) < 1]    
    X_train=np.delete(X_train, drop_idx, axis=0)
    df.drop(drop_idx, axis=0, inplace=True)

    # 정수 시퀀스를 0과 1의 벡터로 변환
    print('>>>> Vectorizing... 정수의 벡터 정제')    
    # 멀티-핫 인코팅
    results=np.zeros((len(X_train), vocab_size), dtype=np.float16)
    for i, sequence in enumerate(X_train):
        for j in sequence:    
            results[i,j]=1.

    return (df,results)


# 모델 만들기
"""
리턴값 : model 객체
"""
def modelDef():
    # 모델정의
    time.sleep(2)
    print('\n>>>> Modeling... 모델 정의')
    model=keras.Sequential([
            layers.Dense(16, activation='relu'),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid'),
        ])

    # 모델 컴파일
    print('>>>> Modeling... 모델 컴파일')
    model.compile(optimizer='rmsprop',
                loss='binary_crossentropy',
                metrics=['accuracy'])
    
    return model

## 모델 검증 훈련
"""
파라미터 : X-train, y_train
리턴값 : model객체, X_train
"""
def modelFit(X_train, y_train):
    # 모델 만들기
    model=modelDef()

    # 데이터 준비
    print('>>>> Modeling... 데이터 셋팅')    
    val_len=int(len(X_train)*0.2)
    X_val=X_train[:val_len].astype(float)
    partial_X_train=X_train[val_len:].astype(float)
    y_val=y_train[:val_len].astype(float)
    partial_y_train=y_train[val_len:].astype(float)
    print('훈련데이터 -리뷰 개수:', len(partial_X_train))
    print('검증데이터 -리뷰 개수:', len(X_val))

    print('\n>>>> Modeling... 모델 훈련 및 검증')
    history=model.fit(
            partial_X_train,
            partial_y_train,
            epochs=15,
            batch_size=124, #512
            validation_data=(X_val, y_val)
        )

    ## 훈련과 검증 손실 그리기   
    print('\n┌──────────────────────────────┐')
    print('│ >> 결과확인 : 손실과 정확도  │')
    print('└──────────────────────────────┘')

    history_dict=history.history
    loss_values=history_dict['loss']
    val_loss_values=history_dict['val_loss']
    epochs=range(1,len(history_dict['loss'])+1)
    plt.plot(epochs, loss_values, 'bo', label='Training loss')
    plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('loss')
    plt.legend()
    plt.show()
    

    ####### 훈련과 검증 정확도 그리기
    plt.clf()
    acc=history_dict['accuracy']
    val_acc=history_dict['val_accuracy']
    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

    print('\n┌──────────────────────────────────────────────────────────────────────┐')
    print('│ >> 결과확인 : Overfitting (과대적합), 에크모를 3회로 조정 후 재실행  │')
    print('└──────────────────────────────────────────────────────────────────────┘')
    time.sleep(3)

    # 모델만들기
    model=modelDef()
    
    print('\n>>>> Modeling... 모델 훈련 및 검증')
    history=model.fit(
            partial_X_train,
            partial_y_train,
            epochs=3,
            batch_size=256)
    results=model.evaluate(X_val, y_val)
    loss_per=results[0]
    accu_per=results[1]
    print('\n┌──────────────────────────────┐')    
    print('│ >> 결과확인 : 손실율 %.2f%s  │' % (loss_per*100, '%'))    
    print('└──────────────────────────────┘')
    print('\n┌──────────────────────────────┐')
    print('│ >> 결과확인 : 정확도 %.2f%s  │' % (accu_per*100,'%'))    
    print('└──────────────────────────────┘')
    print('\n\n')

    return (model, X_train)
    

## 긍정지수 산출
"""
파라미터 : model, X_train,dataframe 객체,columns,table
리턴값 : positive,review numbers
"""
def positiveIdx (model,X_train,df,scols_posi,tab_scrub):
    num=scols_posi[0]
    positive=scols_posi[1]
    posi_data=model.predict(X_train)    
    df[positive]=posi_data
    
    # df.to_csv('naver_review_positive.csv', encoding="UTF-8-sig", index=False)
    
    # 긍정지수 산출 DB 저장    
    print('>>>> Uploading... DB 저장')        
    insQry(tab_scrub,scols_posi,df,3)

    return (df[positive], df[num])





## 영화관 데이터 전처리 
"""
파라미터 : tables, columns
리턴값 : dataframe 객체
"""
def kobisPre(tab_gather,tab_scrub,gcols,scols):
    # 리뷰 데이터 불러오기
    print('\n>>>> Connecting... 데이터베이스 접속')    
    qry='select * from %s;' % (tab_gather)
    kobis_gather=exeSql(qry,'film_innerside',1)
    
    # 날짜 텍스트 처리
    kobis_gather=toText(kobis_gather,'gdate')        

    # 데이터프레임에 담기
    print('\n>>>> Loading... KOBIS 영화관 입장권 데이터')  
    df=dfAppend(kobis_gather,gcols)
    
    # 결측치 Nan처리
    df['ggenre']=df['ggenre'].str.replace('^ +','',regex=True)
    df['gdirec']=df['gdirec'].str.replace('^ +','',regex=True)
    df['ggenre']=df['ggenre'].str.replace('0','')
    df['gdirec']=df['gdirec'].str.replace('0','')
    df['gactor']=df['gactor'].str.replace('0','')    
    df['ggenre'].replace('', np.nan, inplace=True)
    df['gdirec'].replace('', np.nan, inplace=True)
    df['gactor'].replace('', np.nan, inplace=True)
    df['gaudience'].replace(0, np.nan, inplace=True)    
    
    #한글,숫자,영문,한칸공백이외 정제
    df['gmovie']=df['gmovie'].str.replace('^ +|\'',' ',regex=True)    
    df['gdirec']=df['gdirec'].str.replace('[^ ㄱ-ㅎㅏ-ㅡ가-힣0-9a-zA-Z,]','',regex=True)    
    df['gactor']=df['gactor'].str.replace('[^ ㄱ-ㅎㅏ-ㅡ가-힣0-9a-zA-Z,]','',regex=True)    
    df['gmovie_id']=df['gmovie_id'].str.replace('[^ ㄱ-ㅎㅏ-ㅡ가-힣0-9a-zA-Z\]\[,-]','',regex=True)    

    # NaN 값 제거    
    df=df.dropna(subset=['gaudience'], how='any', axis=0)
    print('>>>> Refinementing... 결측치 정제')       
    time.sleep(0.5)

    # DB 저장
    print('>>>> Uploading... DB 저장')
    insQry(tab_scrub,scols,df,2)
    
    return df



# 영화관 입장권 데이터 불러오기
"""
파라미터 : columns, table
리턴값 : dataframe 객체
"""
def kobisLoad(movie,audience,tab_scrub):
    ## 데이터 불러오기: 리뷰, 라벨(긍정,부정), 리뷰번호         
    print('\n>>>> Connecting... 데이터베이스 접속')    
    qry='select %s,%s from %s;' % (movie,audience,tab_scrub)
    movie_scrub=exeSql(qry,'film_innerside',1)            
    
    # 데이터프레임에 담기
    print('>>>> Loading... KOBIS 영화관 입장권 데이터')    
    df=dfAppend(movie_scrub,[movie,audience])

    return df
    
    
# 네이버 영화 리뷰 데이터 불러오기
"""
파라미터 : columns, table
리턴값 : dataframe 객체
"""
def reviewLoad(movie,review,sumpoint,positive,tab_scrub):    
    ## 데이터 불러오기        
    print('\n>>>> Connecting... 데이터베이스 접속')    
    qry='select %s,%s,%s,%s from %s;' % (movie,review,sumpoint,positive,tab_scrub)
    rev_scrub=exeSql(qry,'film_innerside',1)        
    
    # 데이터프레임에 담기
    print('>>>> Loading... 네이버 영화 리뷰 데이터')        
    df=dfAppend(rev_scrub,[movie,review,sumpoint,positive])

    return df

