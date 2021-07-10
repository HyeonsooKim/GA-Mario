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

        self.label = QLabel(self)

        self.show()

    #키를 누를 때
    def keyPressEvent(self, event):
        key = event.key()
        print(str(key) + ' press')
        self.label.setText(str(key) + ' press')

    #키를 뗄 때
    def keyReleaseEvent(self, event):
        key = event.key()
        self.setlab(str(key) + ' release')
        self.label.setText(str(key) + ' released')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())
