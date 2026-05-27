import sqlite3
from datetime import datetime
import random


class ProductManager:
    """SQLite를 사용한 전자제품 데이터 관리 클래스"""
    
    def __init__(self, db_name="MyProduct.db"):
        """
        데이터베이스를 새로 만들고 준비하는 함수
        
        이 함수가 하는 일:
        - 데이터를 저장할 파일(데이터베이스)을 만든다
        - 그 파일과 연결한다
        - 제품 정보를 저장할 테이블을 준비한다
        
        매개변수:
            db_name (str): 만들 데이터베이스 파일의 이름
                          기본값은 "MyProduct.db" (원하면 다른 이름 사용 가능)
        
        사용 예시:
            pm = ProductManager()  # "MyProduct.db" 파일 자동 생성
            pm = ProductManager("MyShop.db")  # "MyShop.db" 파일 생성
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """
        데이터베이스 파일과 연결하는 함수
        
        이 함수가 하는 일:
        - 저장된 데이터베이스 파일을 찾아 열어서 준비한다
        - 데이터를 읽고 쓸 수 있도록 도구(cursor)를 준비한다
        - 연결 성공 또는 실패 메시지를 출력한다
        
        반환값: 없음 (하지만 내부적으로 self.conn과 self.cursor를 설정)
        
        사용 예시:
            pm = ProductManager()
            # 자동으로 connect()가 호출됨
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"✓ {self.db_name} 데이터베이스 연결 성공")
        except sqlite3.Error as e:
            print(f"✗ 데이터베이스 연결 실패: {e}")
    
    def create_table(self):
        """
        제품 정보를 저장할 테이블을 만드는 함수
        
        이 함수가 하는 일:
        - "Products" 라는 이름의 표를 만든다
        - 표에는 3개의 열이 있다:
          * productID: 제품 번호 (자동으로 1, 2, 3... 증가)
          * productName: 제품 이름 (예: "스마트폰")
          * productPrice: 제품 가격 (예: 500000)
        - 이미 있는 테이블은 다시 만들지 않는다
        
        반환값: 없음
        
        사용 예시:
            pm = ProductManager()  # 자동으로 create_table() 호출됨
        """
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                    productID INTEGER PRIMARY KEY AUTOINCREMENT,
                    productName TEXT NOT NULL,
                    productPrice INTEGER NOT NULL
                )
            ''')
            self.conn.commit()
            print("✓ Products 테이블 준비 완료")
        except sqlite3.Error as e:
            print(f"✗ 테이블 생성 실패: {e}")
    
    def insert(self, product_name, product_price):
        """
        새로운 제품 한 개를 저장하는 함수
        
        이 함수가 하는 일:
        - 새 제품의 이름과 가격을 받아서
        - 데이터베이스에 저장한다
        - 저장한 제품의 번호(ID)를 반환한다
        
        매개변수:
            product_name (str): 제품의 이름 (예: "갤럭시폰")
            product_price (int): 제품의 가격 (예: 1000000)
        
        반환값:
            int: 새로 저장된 제품의 ID 번호
            None: 저장에 실패했을 때
        
        사용 예시:
            pm = ProductManager()
            new_id = pm.insert("아이폰", 1500000)
            print(new_id)  # 저장된 제품의 번호 출력
        """
        try:
            self.cursor.execute('''
                INSERT INTO Products (productName, productPrice)
                VALUES (?, ?)
            ''', (product_name, product_price))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"✗ INSERT 실패: {e}")
            return None
    
    def insert_many(self, data_list):
        """
        많은 제품들을 한꺼번에 저장하는 함수
        
        이 함수가 하는 일:
        - 여러 개의 제품 정보를 한 번에 받아서
        - 모두 데이터베이스에 빠르게 저장한다
        - 몇 개를 저장했는지 메시지로 알려준다
        
        매개변수:
            data_list (list): 제품 정보 목록
                             각 항목은 (제품명, 가격) 형태
                             예: [("아이폰", 1500000), ("갤럭시", 1000000)]
        
        반환값:
            bool: 저장 성공하면 True, 실패하면 False
        
        사용 예시:
            pm = ProductManager()
            products = [("아이폰", 1500000), ("갤럭시", 1000000)]
            pm.insert_many(products)  # 2개 데이터 한번에 저장
        """
        try:
            self.cursor.executemany('''
                INSERT INTO Products (productName, productPrice)
                VALUES (?, ?)
            ''', data_list)
            self.conn.commit()
            print(f"✓ {len(data_list)}개 데이터 INSERT 완료")
            return True
        except sqlite3.Error as e:
            print(f"✗ INSERT 실패: {e}")
            return False
    
    def select_all(self):
        """
        데이터베이스에 저장된 모든 제품을 보는 함수
        
        이 함수가 하는 일:
        - 저장된 모든 제품의 정보를 불러온다
        - 각 제품의 ID, 이름, 가격을 모두 보여준다
        
        반환값:
            list: 모든 제품 정보 목록
                 비어있으면 빈 목록 반환
        
        사용 예시:
            pm = ProductManager()
            all_products = pm.select_all()
            for product in all_products:
                print(product)  # (ID, 제품명, 가격) 출력
        """
        try:
            self.cursor.execute('SELECT * FROM Products')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ SELECT 실패: {e}")
            return []
    
    def select_by_id(self, product_id):
        """
        제품 번호(ID)로 특정 제품을 찾는 함수
        
        이 함수가 하는 일:
        - 찾고 싶은 제품의 번호를 받아서
        - 그 제품이 맞는지 확인하고 정보를 보여준다
        
        매개변수:
            product_id (int): 찾을 제품의 번호 (예: 5)
        
        반환값:
            tuple: 찾은 제품의 정보 (ID, 제품명, 가격)
            None: 그 번호의 제품이 없으면 None
        
        사용 예시:
            pm = ProductManager()
            product = pm.select_by_id(1)
            if product:
                print(product)  # (1, "아이폰", 1500000) 출력
        """
        try:
            self.cursor.execute('SELECT * FROM Products WHERE productID = ?', (product_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"✗ SELECT 실패: {e}")
            return None
    
    def select_by_name(self, product_name):
        """
        제품 이름으로 찾는 함수
        
        이 함수가 하는 일:
        - 찾고 싶은 제품의 이름을 받아서
        - 그 이름이 들어있는 모든 제품을 찾는다
        - 찾은 모든 제품들의 정보를 보여준다
        
        매개변수:
            product_name (str): 찾을 제품 이름의 일부 (예: "폰")
                               "갤럭시폰", "아이폰"이 모두 검색됨
        
        반환값:
            list: 찾은 제품들의 정보 목록
                 아무것도 안 나오면 빈 목록
        
        사용 예시:
            pm = ProductManager()
            phones = pm.select_by_name("폰")
            print(f"찾은 제품: {len(phones)}개")  # 이름에 '폰'이 들어간 제품 개수
        """
        try:
            self.cursor.execute('SELECT * FROM Products WHERE productName LIKE ?', (f'%{product_name}%',))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ SELECT 실패: {e}")
            return []
    
    def select_by_price_range(self, min_price, max_price):
        """
        가격 범위로 제품을 찾는 함수
        
        이 함수가 하는 일:
        - 최소 가격과 최대 가격을 받아서
        - 그 사이에 있는 모든 제품을 찾는다
        - 가격이 싼 것부터 비싼 것 순서로 보여준다
        
        매개변수:
            min_price (int): 최소 가격 (예: 100000)
            max_price (int): 최대 가격 (예: 500000)
        
        반환값:
            list: 가격 범위에 맞는 제품들의 정보 목록
                 (가격 순서로 정렬됨)
        
        사용 예시:
            pm = ProductManager()
            budget_products = pm.select_by_price_range(100000, 500000)
            for product in budget_products:
                print(product)  # 10만원~50만원 제품 출력
        """
        try:
            self.cursor.execute('''
                SELECT * FROM Products 
                WHERE productPrice BETWEEN ? AND ?
                ORDER BY productPrice
            ''', (min_price, max_price))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ SELECT 실패: {e}")
            return []
    
    def update(self, product_id, product_name=None, product_price=None):
        """
        저장된 제품의 정보를 바꾸는 함수
        
        이 함수가 하는 일:
        - 제품 번호를 받아서 그 제품을 찾고
        - 이름이나 가격을 새로운 정보로 바꾼다
        - 변경 성공 또는 실패 메시지를 알려준다
        
        매개변수:
            product_id (int): 바꿀 제품의 번호 (필수)
            product_name (str): 새로운 제품 이름 (선택, 안 하면 원래대로)
            product_price (int): 새로운 제품 가격 (선택, 안 하면 원래대로)
        
        반환값:
            bool: 수정 성공하면 True, 실패하면 False
        
        사용 예시:
            pm = ProductManager()
            pm.update(1, "새 아이폰", 2000000)  # 이름과 가격 둘 다 변경
            pm.update(2, product_price=1500000)  # 가격만 변경
        """
        try:
            if product_name and product_price:
                self.cursor.execute('''
                    UPDATE Products 
                    SET productName = ?, productPrice = ?
                    WHERE productID = ?
                ''', (product_name, product_price, product_id))
            elif product_name:
                self.cursor.execute('''
                    UPDATE Products 
                    SET productName = ?
                    WHERE productID = ?
                ''', (product_name, product_id))
            elif product_price:
                self.cursor.execute('''
                    UPDATE Products 
                    SET productPrice = ?
                    WHERE productID = ?
                ''', (product_price, product_id))
            else:
                print("✗ 수정할 항목이 없습니다")
                return False
            
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"✓ productID {product_id} 수정 완료")
                return True
            else:
                print(f"✗ productID {product_id}을(를) 찾을 수 없습니다")
                return False
        except sqlite3.Error as e:
            print(f"✗ UPDATE 실패: {e}")
            return False
    
    def delete(self, product_id):
        """
        저장된 제품을 지우는 함수
        
        이 함수가 하는 일:
        - 제품 번호를 받아서
        - 그 제품을 데이터베이스에서 삭제한다
        - 삭제 성공 또는 실패 메시지를 알려준다
        
        매개변수:
            product_id (int): 지울 제품의 번호 (예: 5)
        
        반환값:
            bool: 삭제 성공하면 True, 실패하면 False
        
        사용 예시:
            pm = ProductManager()
            pm.delete(1)  # 번호 1인 제품 삭제
        """
        try:
            self.cursor.execute('DELETE FROM Products WHERE productID = ?', (product_id,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"✓ productID {product_id} 삭제 완료")
                return True
            else:
                print(f"✗ productID {product_id}을(를) 찾을 수 없습니다")
                return False
        except sqlite3.Error as e:
            print(f"✗ DELETE 실패: {e}")
            return False
    
    def delete_all(self):
        """
        데이터베이스에 저장된 모든 제품을 지우는 함수
        
        이 함수가 하는 일:
        - 저장된 모든 제품을 한꺼번에 삭제한다
        - 지운 제품의 개수를 메시지로 알려준다
        
        반환값:
            bool: 삭제 성공하면 True, 실패하면 False
        
        주의: 이 함수를 실행하면 모든 데이터가 사라집니다!
        
        사용 예시:
            pm = ProductManager()
            pm.delete_all()  # 모든 제품 삭제
        """
        try:
            self.cursor.execute('DELETE FROM Products')
            self.conn.commit()
            count = self.cursor.rowcount
            print(f"✓ {count}개 데이터 삭제 완료")
            return True
        except sqlite3.Error as e:
            print(f"✗ DELETE 실패: {e}")
            return False
    
    def get_count(self):
        """
        저장된 제품이 몇 개인지 세는 함수
        
        이 함수가 하는 일:
        - 데이터베이스에 저장된 제품의 개수를 센다
        - 그 개수를 숫자로 알려준다
        
        반환값:
            int: 저장된 제품의 개수
        
        사용 예시:
            pm = ProductManager()
            total = pm.get_count()
            print(f"총 {total}개의 제품이 있습니다")  # 총 1000개의 제품이 있습니다
        """
        try:
            self.cursor.execute('SELECT COUNT(*) FROM Products')
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print(f"✗ COUNT 실패: {e}")
            return 0
    
    def get_statistics(self):
        """
        제품들의 통계를 보는 함수
        
        이 함수가 하는 일:
        - 저장된 모든 제품의 통계를 계산한다:
          * total: 제품 총 개수
          * min_price: 가장 싼 제품의 가격
          * max_price: 가장 비싼 제품의 가격
          * avg_price: 모든 제품의 평균 가격
        
        반환값:
            dict: 통계 정보 딕셔너리
                 {'total': 1000, 'min_price': 10000, 'max_price': 999999, 'avg_price': 500000}
            None: 조회 실패시
        
        사용 예시:
            pm = ProductManager()
            stats = pm.get_statistics()
            print(f"평균 가격: {stats['avg_price']:,}원")  # 평균 가격: 500,000원
        """
        try:
            self.cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    MIN(productPrice) as min_price,
                    MAX(productPrice) as max_price,
                    AVG(productPrice) as avg_price
                FROM Products
            ''')
            result = self.cursor.fetchone()
            return {
                'total': result[0],
                'min_price': result[1],
                'max_price': result[2],
                'avg_price': round(result[3], 2) if result[3] else 0
            }
        except sqlite3.Error as e:
            print(f"✗ 통계 조회 실패: {e}")
            return None
    
    def close(self):
        """
        데이터베이스와의 연결을 끊는 함수
        
        이 함수가 하는 일:
        - 데이터베이스 파일을 안전하게 닫는다
        - 프로그램이 끝나기 전에 반드시 실행해야 한다
        
        반환값: 없음
        
        사용 예시:
            pm = ProductManager()
            # ... 여러 작업 수행 ...
            pm.close()  # 프로그램 끝낼 때 반드시 실행
        """
        if self.conn:
            self.conn.close()
            print("✓ 데이터베이스 연결 종료")


def generate_sample_data():
    """
    테스트용 샘플 제품 데이터 1만개를 만드는 함수
    
    이 함수가 하는 일:
    - 실제 전자제품 이름들(스마트폰, 노트북 등) 중에서 무작위로 선택
    - 각 제품마다 번호를 붙여서 이름을 만든다 (예: "스마트폰 1")
    - 각 제품마다 무작위 가격을 정한다 (10,000원 ~ 1,000,000원)
    - 이렇게 만든 1만개의 제품 정보를 목록으로 반환한다
    
    반환값:
        list: 1만개의 (제품명, 가격) 데이터
    
    사용 예시:
        sample_data = generate_sample_data()
        print(len(sample_data))  # 10000 출력
        print(sample_data[0])  # 첫 번째 샘플 데이터 출력
    """
    products = [
        "스마트폰", "노트북", "태블릿", "이어폰", "스마트워치",
        "모니터", "키보드", "마우스", "헤드폰", "스피커",
        "카메라", "프린터", "라우터", "그래픽카드", "SSD",
        "램", "파워서플라이", "쿨러", "케이스", "케이블"
    ]
    
    data_list = []
    for i in range(1, 10001):
        product_name = f"{random.choice(products)} {i}"
        product_price = random.randint(10000, 1000000)
        data_list.append((product_name, product_price))
    
    return data_list


def main():
    """
    프로그램 전체를 실행하고 모든 기능을 테스트하는 함수
    
    이 함수가 하는 일:
    1. ProductManager 객체를 만든다 (데이터베이스 생성)
    2. 샘플 데이터 1만개를 생성해서 저장한다
    3. 모든 기능을 하나씩 테스트한다:
       - INSERT: 새 제품 추가
       - SELECT: 제품 검색 (ID로, 이름으로, 가격으로)
       - UPDATE: 제품 정보 수정
       - DELETE: 제품 삭제
    4. 통계 정보를 보여준다
    5. 데이터베이스 연결을 끝낸다
    
    반환값: 없음
    
    사용 예시:
        # 프로그램 실행하면 main() 함수가 자동으로 실행됨
    """
    print("=" * 60)
    print("SQLite 전자제품 데이터 관리 시스템")
    print("=" * 60)
    
    # 데이터베이스 매니저 초기화
    pm = ProductManager("MyProduct.db")
    
    print("\n[1] 샘플 데이터 생성 및 삽입 중...")
    # 기존 데이터 삭제
    pm.delete_all()
    
    # 샘플 데이터 1만개 생성
    sample_data = generate_sample_data()
    pm.insert_many(sample_data)
    
    print("\n[2] 전체 데이터 통계")
    stats = pm.get_statistics()
    print(f"   총 제품 수: {stats['total']}개")
    print(f"   최소 가격: {stats['min_price']:,}원")
    print(f"   최대 가격: {stats['max_price']:,}원")
    print(f"   평균 가격: {stats['avg_price']:,}원")
    
    print("\n[3] 단건 INSERT 테스트")
    new_id = pm.insert("삼성 갤럭시 Z폴드5", 2500000)
    print(f"   생성된 ID: {new_id}")
    
    print("\n[4] SELECT 테스트")
    print("   - ID로 조회 (ID=1):")
    product = pm.select_by_id(1)
    if product:
        print(f"     ID: {product[0]}, 제품명: {product[1]}, 가격: {product[2]:,}원")
    
    print("   - 제품명으로 조회 ('스마트폰'):")
    products = pm.select_by_name("스마트폰")
    print(f"     검색 결과: {len(products)}개")
    if products:
        for p in products[:3]:
            print(f"     ID: {p[0]}, 제품명: {p[1]}, 가격: {p[2]:,}원")
        print(f"     ... (이하 {len(products)-3}개 생략)")
    
    print("   - 가격 범위 조회 (100,000 ~ 200,000원):")
    price_products = pm.select_by_price_range(100000, 200000)
    print(f"     검색 결과: {len(price_products)}개")
    if price_products:
        for p in price_products[:3]:
            print(f"     ID: {p[0]}, 제품명: {p[1]}, 가격: {p[2]:,}원")
        print(f"     ... (이하 {len(price_products)-3}개 생략)")
    
    print("\n[5] UPDATE 테스트")
    pm.update(1, "Apple iPhone 15 Pro", 1500000)
    updated = pm.select_by_id(1)
    if updated:
        print(f"   수정 후: ID: {updated[0]}, 제품명: {updated[1]}, 가격: {updated[2]:,}원")
    
    print("\n[6] DELETE 테스트")
    pm.delete(10001)
    print(f"   현재 데이터 개수: {pm.get_count()}개")
    
    print("\n[7] 최종 통계")
    final_stats = pm.get_statistics()
    print(f"   총 제품 수: {final_stats['total']}개")
    print(f"   최소 가격: {final_stats['min_price']:,}원")
    print(f"   최대 가격: {final_stats['max_price']:,}원")
    print(f"   평균 가격: {final_stats['avg_price']:,}원")
    
    # 데이터베이스 연결 종료
    pm.close()
    print("\n" + "=" * 60)
    print("프로그램 종료")
    print("=" * 60)


if __name__ == "__main__":
    main()
