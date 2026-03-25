import sqlite3
import random

class ProductDatabase:
    def __init__(self, db_name='MyProduct.db'):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                            productID INTEGER PRIMARY KEY,
                            productName TEXT,
                            productPrice INTEGER
                          )''')
        conn.commit()
        conn.close()

    def insert(self, productID, productName, productPrice):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Products (productID, productName, productPrice) VALUES (?, ?, ?)",
                       (productID, productName, productPrice))
        conn.commit()
        conn.close()

    def update(self, productID, productName=None, productPrice=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        if productName and productPrice:
            cursor.execute("UPDATE Products SET productName=?, productPrice=? WHERE productID=?",
                           (productName, productPrice, productID))
        elif productName:
            cursor.execute("UPDATE Products SET productName=? WHERE productID=?", (productName, productID))
        elif productPrice:
            cursor.execute("UPDATE Products SET productPrice=? WHERE productID=?", (productPrice, productID))
        conn.commit()
        conn.close()

    def delete(self, productID):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Products WHERE productID=?", (productID,))
        conn.commit()
        conn.close()

    def select(self, productID=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        if productID:
            cursor.execute("SELECT * FROM Products WHERE productID=?", (productID,))
            result = cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM Products")
            result = cursor.fetchall()
        conn.close()
        return result

# 샘플 데이터 10만 개 생성 및 삽입
if __name__ == "__main__":
    db = ProductDatabase()
    for i in range(1, 100001):
        name = f"전자제품 {i}"
        price = random.randint(1000, 100000)
        db.insert(i, name, price)
    print("10만 개의 샘플 데이터가 삽입되었습니다.")