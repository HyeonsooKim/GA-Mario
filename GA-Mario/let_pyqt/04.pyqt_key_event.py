#04. pyqt_key_event.py
#PyQt 키 이벤트

import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
import numpy as np

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(300, 400)

        self.setWindowTitle('GA Mario')

        self.label_text = QLabel(self)
        self.label_text.setGeometry(0, 0, 100, 100)
        self.show()

    #키를 누를 때
    def keyPressEvent(self, event):
        key = event.key()
        a = str(key) + ' press'
        #global a    #전역변수를 찾는 코드
        print(a)
        self.label_text.setText(a)
        if key == Qt.Key_F1:    #F1키 누르면 코드 실행, 예외처리 가능
            print('f1 key')


    #키를 뗄 때
    def keyReleaseEvent(self, event):
        key = event.key()
        b = str(key) + ' release'
        print(b)

        self.label_text.setText(b)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
