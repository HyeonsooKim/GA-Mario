#05.pyqt_timer.py
# PyQt 타이머 예제
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QTimer

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        #창 크기 고정
        self.setFixedSize(400, 300)
        #창 제목 설정
        self.setWindowTitle('My Window')

        self.label_text = QLabel(self)
        self.label_text.setGeometry(50, 50, 150, 150)

        # 창 띄우기
        self.show()

        #타이머 생성
        qtimer = QTimer(self)
        #타이머에 실행할 함수 연결
        qtimer.timeout.connect(self.timer)   #타임아웃이라는 함수가 실행될 때 타이머를 call

        #1초마다 연결된 함수를 실행
        qtimer.start(1000)
        self.cnt=0

        #버튼 클릭할 때~
        #button.clicked.connect(~)

    # 주기적으로 실행할 함수
    def timer(self):
        # self.cnt += 1
        # a = str(self.cnt)
        # self.label_text.setText(a)  #string 형식만 출력가능하나봄
        print('Timer')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec())