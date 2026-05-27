# 내장라이브러리.py

import random

print(random.random())
print(random.random())

print(random.uniform(2.0, 5.0))
print(random.uniform(2.0, 5.0))

# 리스트에서 랜덤하게 선택
items = ['apple', 'banana', 'cherry', 'date', 'elderberry']
print(random.choice(items))
print(random.choice(items))

# 루프를 돌면서 0~19 사이의 랜덤한 숫자 10개 생성
print([random.randrange(20) for i in range(10)])
print([random.randrange(20) for i in range(10)])

# 샘플링
print(random.sample(range(20), 10))
print(random.sample(range(20), 10))
print(random.sample(range(20), 10))

# lotto 번호 생성
print(random.sample(range(1, 46), 6))

# 파일명 다루기
import os.path
fileName = "c:\\python313\\python.exe"
print(os.path.basename(fileName))  # 파일명 추출
print(os.path.abspath("python.exe"))   # 절대 경로 추출

if os.path.exists(fileName):
    print("파일의 크기 : {0}".format(os.path.getsize(fileName)))
else:
    print("파일이 존재하지 않습니다.")

# 운영체제의 정보
import os

print("운영체제 이름 : {0}".format(os.name))
print("운영체제 환경변수 : {0}".format(os.environ))
os.system("notepad.exe")  # 메모장 실행 


# 특정폴더의 파일리스트
import glob
print(glob.glob("c:\\work\\*.*"))

for item in glob.glob("c:\\work\\*.*"):
    print(item)
    