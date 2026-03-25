# db1.py
import sqlite3

#메모리에 임시로 저장
con = sqlite3.connect(':memory:')
#커서객체 리턴
cur  = con.cursor()
#테이블 생성
cur.execute("create table Phonebook (Name text, PhoneNum text);")
#데이터 삽입
cur.execute("insert into Phonebook values('홍길동', '010-1234-5678');")
#매개변수로 입력
name = "전우치"
phone = "010-1234-5678"
cur.execute("insert into Phonebook values(?, ?);", (name, phone))
#다중 데이터를 입력
datalist = (('김철수', '010-1234-5678'), ('박영희', '010-1234-5678'))
cur.executemany("insert into Phonebook values(?, ?);", datalist)

#데이터 조회 : 블럭 주석 처리(ctrl + /)
# for row in cur.execute("select * from Phonebook;"):
#     print(row)

cur.execute("select * from Phonebook;")
print("---fetchone()---")
print(cur.fetchone())
print("---fetchmany(2)---")
print(cur.fetchmany(2))
print("---fetchall()---")
cur.execute("select * from Phonebook;")
print(cur.fetchall())

#연결 종료
con.close()