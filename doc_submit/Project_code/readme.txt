=================================================================================
[ ������Ʈ ���� ���� ]
Project_code > 
	main_full.py	- ���̹� ��ȭ ���� ���������� ��ó�� �� �����м�, ��ȭ�� ����� ������ ��ó��	** ��������
	dataGather.py 	- DB ����								** ��������
	naver_movie_review.py	- ���̹� ��ȭ ���� ũ�ѷ�					** ��������
	kobis_crawling_vscode.py	- KOBIS ��ȭ�� ����� ũ�ѷ�					** ��������
	dataScrub.py	- ������ ��ó�� �� �����м� ���� �Լ�
	dbProc.py		- db ���� �Լ�
	DB_ver0.1.sql	- db ���� ����
Project_code > data
	stopwords.txt	- �ҿ��
=================================================================================


[ ������ ȯ�� ���� ]

################ Visual Studio Code Ȯ���� ��ġ
- python
- python for VSCode
- Python Extension Pack
- Code Runner

################ Visual Studio Code Ȯ���� - Code Runner ��������
1. ������ �÷����� â���� code runner�� �˻��ؼ� ��Ϲ�Ƣ ��ư�� ���� �� Extension Settings ( Ȯ�弳�� ) �� ����
2. �߰� �뿡 �ִ� Code-runner : Run In Terminal �� üũ


################  java JSK ��ġ
https://www.oracle.com/java/technologies/downloads/#jdk19-windows
1. �ٿ�ε� : Java 19 > Windows > x64 Installer
2. �ý��� ȯ�� ���� ����
   ����ǻ�� - ��Ŭ�� �Ӽ� - ��� �ý��� ���� - ��� - ȯ�� ����
   User�� ���� ����� ���� -  Path  - �����Ͽ� �߰�
%JAVA_HOME%bin

3. �ý��� ���� - ���θ�����Ͽ� �߰�
�����̸� : JAVA_HOME
������ : C:\Program Files\Java\jdk-19


################  mySQL ��ġ
http://dev.mysql.com/downloads/
1. MySQL��ġ���� �ٿ�ε� : mysql-installer-community-8.0.30.0.msi
2. �ý��� ȯ�� ���� ����
   ����ǻ�� - ��Ŭ�� �Ӽ� - ��� �ý��� ���� - ��� - ȯ�� ����
   User�� ���� ����� ���� -  Path  - �����Ͽ� �߰�
C:\Program Files\MySQL\MySQL Server 8.0\bin


################ CUDA �ֽ� ���� �ٿ�ε�
https://developer.nvidia.com/cuda-toolkit-archive

1. Download Lastest CUDA Toolkit �ٿ�ε� �� ��ġ ����
2. �ý��� ȯ�� ���� ����
����ǻ�� - ��Ŭ�� �Ӽ� - ��� �ý��� ���� - ��� - ȯ�� ����
�ý��� ������ Path �����Ͽ� �߰�
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\bin
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.4\libnvvp


################ Visual Studio Code ����ȯ�� ����
(�����Ʃ���)
(�͹̳�)
1. virtualenv ��� ��ġ
pip install virtualenv

2. ����ȯ�� ����
virtualenv venv --python=3.10.6

3. ����ȯ�� ����
.\venv\Scripts\activate

//����ȯ�� ���� �� ���� ���� �߻��� - case1
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
(�Ǵ� Set-ExecutionPolicy Unrestricted)

//����ȯ�� ���� �� ���� ���� �߻��� - case2
case1 �� �����ص�, ��ũ��Ʈ ���� ���θ� Ȯ���� ��
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser

4. ���������� ����
(�����Ʃ���) -> ctrl+shift+P -> Python 3.10.6('venv':venv) ����

5. ��� ��ġ
pip install -r requiremnets.txt

//fatal error ���� �߻��� 
python -m pip install -r requiremnets.txt


################ Visual Studio Code ��Ű�� ��ġ
�͹̳� â���� pip install -r requirements.txt �Է�

���� �߻��� ��Ű�� ���� ��ġ







