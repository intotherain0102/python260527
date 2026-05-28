# DemoForm.py
# DemoForm.ui 파일에서 생성된 UI 클래스를 가져옵니다.

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt6 import uic

#  디자인 파일 로딩
form_class = uic.loadUiType("DemoForm.ui")[0]

# 폼 클래스를 정의
class DemoForm(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 초기화 
        self.label.setText("이렇게 화면에 출력")  # 라벨 텍스트 설정

# 진입점 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    demo = DemoForm()  # 폼 클래스 인스턴스 생성
    demo.show()  # 폼 표시
    sys.exit(app.exec())  # 이벤트 루프 실행


