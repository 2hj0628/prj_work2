import subprocess
import sys

try:
    import pymysql
    import pandas as pd
    from tqdm import tqdm 
except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pymysql'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pandas'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'tqdm'])
finally:    
    import pymysql
    import pandas as pd
    from tqdm import tqdm
    import time


host='localhost'
# db='film_innerside'
user='root'
pw='1234'
charset='utf-8'
port=3306



#실행 함수
def exeSql(sql,database,opt=1):    
    try:
        with pymysql.connect(host=host,user=user,password=pw,db=database,port=port) as conn:
            #pymysql.cursors.DictCursor 딕셔너리 형태로
            cur=conn.cursor(pymysql.cursors.DictCursor) 
            sqls=sql.split(';')
            for sql in sqls:
                if len(sql)>0:                
                    result=cur.execute(sql)                
            if opt==1:
                result=cur.fetchall()
            conn.commit() #auto 커밋 true
    
    except pymysql.err.OperationalError:        
        print('OperationalError: DB 연결에 에러가 발생하였습니다. ')

    return (result)




#%%
# DB 저장 함수
def insQry(_table,_cols,_df,intype=0):
    df_size=_df.shape  
    cnt=1
    sql=''
    with tqdm(total=df_size[0]) as pbar:
        for idx, data in _df.iterrows():
            data=data.values.tolist()
            # intype1: 리뷰 정제 저장
            if intype==1:                
                words=data[3]
                words="/".join(words)
                sql='INSERT INTO {} ({},{},{},{},{},{},{}) VALUES ('"'{}'"','"'{}'"','"'{}'"',{},{},'"'{}'"',{});{}'.format(_table,_cols[0],_cols[1],_cols[2],_cols[3],_cols[4],_cols[5],_cols[6],data[1],data[2],words,data[4],data[5],data[6],data[-1],sql)
                cnt+=1
                pbar.update(1)
            
            # intype2: 데이터 저장 정제, 컬럼수:영화관입장권 테이블
            elif intype==2:                
                sql='INSERT INTO {} ({},{},{},{},{},{},{},{}) VALUES ('"'{}'"','"'{}'"',{},'"'{}'"','"'{}'"','"'{}'"','"'{}'"','"'{}'"') ON DUPLICATE KEY UPDATE {}={};{}'.format(_table,_cols[0],_cols[1],_cols[2],_cols[3],_cols[4],_cols[5],_cols[6],_cols[7],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[-1],_cols[2],data[3],sql)
                cnt+=1
                pbar.update(1)
            
            # intype3: 긍정지수 추가
            elif intype==3:
                num=_cols[0]
                posi=_cols[1]
                sql='INSERT INTO {} ({},{})  VALUES ({},'"'{}'"')  ON DUPLICATE KEY UPDATE  {}={};{}'.format(_table,posi,num,data[-1],data[-2],posi,data[-1],sql)
                cnt+=1                
                pbar.update(1)
            
            # intype0
            else:
                sql='INSERT INTO `{}` ({})  VALUES '"'{}'"';{}'.format(_table,_cols[0],data[0],sql)
                cnt+=1
            
            if cnt%30==0 or cnt==len(_df):
                # print(sql)
                exeSql(sql,'film_innerside',0)
                sql=''
