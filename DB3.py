from ProductDB import ProductDatabase

db = ProductDatabase()
db.insert(100001, "새 전자제품", 50000)  # 삽입
db.update(1, productName="업데이트된 제품")  # 업데이트
db.delete(2)  # 삭제
products = db.select()  # 모든 제품 조회
product = db.select(1)  # 특정 제품 조회
