# DB연습2.py

import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('c:\\work\\sample.db')
##conn = sqlite3.connect(":memory:")

cursor = conn.cursor()

# 테이블 생성
cursor.execute('''CREATE TABLE IF NOT EXISTS PhoneBook
                 (Name text PRIMARY KEY, Phone text)''')

# 데이터 삽입
cursor.execute("INSERT INTO PhoneBook (Name, Phone) VALUES (?, ?)", ("Alice1", "123-456-7890"))
cursor.execute("INSERT INTO PhoneBook (Name, Phone) VALUES (?, ?)", ("Bob1", "098-765-4321"))

# 여러 데이터 삽입
datalist = [("Charlie1", "555-555-5555"), ("David1", "444-444-4444")]
cursor.executemany("INSERT INTO PhoneBook (Name, Phone) VALUES (?, ?)", datalist)

# 변경 사항 저장
conn.commit()

# 데이터 조회
cursor.execute("SELECT * FROM PhoneBook")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 연결 닫기
conn.close()
