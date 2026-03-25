# DB2.py
import sqlite3

#영구적으로 파일에 저장(raw string notation)
con = sqlite3.connect(r"c:\work\sample2.db")

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
for row in cur.execute("select * from Phonebook;"):
    print(row)

#작업 완료
#con.commit()

#연결 종료
con.close()