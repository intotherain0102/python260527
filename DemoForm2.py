# DemoForm2.py
# DemoForm2.ui 파일에서 생성된 UI 클래스를 가져옵니다.

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt6 import uic

# 웹 크롤링에 필요한 라이브러리
from bs4 import BeautifulSoup
import urllib.request
# 정규표현식
import re


#  디자인 파일 로딩
form_class = uic.loadUiType("DemoForm2.ui")[0]

# 폼 클래스를 정의
class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 초기화 
    # 슬롯 메소드 정의
    def firstClick(self):

        #User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
        hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}

        # 파일에 저장(write text)
        f = open("todayHumor.txt", "wt", encoding="utf-8")

        #url = "https://www.clien.net/service/board/sold"

        # 페이지 번호를 1부터 10까지 증가시키면서 반복
        for i in range(1, 11):
            url = "https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=" + str(i)

            print(url)

            #웹브라우져 헤더 추가 
            req = urllib.request.Request(url, headers = hdr)
            data = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(data, "html.parser")

            # filtering
            list = soup.find_all("td", attrs={"class":"subject"})

            for tag in list:
                title = tag.find("a").text.strip()

                # 정규표현식으로 문자열 가공
                if re.search("일본", title):
                    print(title)
                    f.write(title + "\n")

        f.close()

        self.label.setText("오늘의 유머 - 일본관련 게시물 검색 완료!")
    def secondClick(self):
        self.label.setText("두 번째 버튼이 클릭되었습니다.!!")
    def thirdClick(self):
        self.label.setText("세 번째 버튼이 클릭되었습니다.!!!")

# 진입점 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    demo = DemoForm()  # 폼 클래스 인스턴스 생성
    demo.show()  # 폼 표시
    sys.exit(app.exec())  # 이벤트 루프 실행


