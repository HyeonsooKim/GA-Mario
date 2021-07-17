# 03. get_screen.py
# 게임 화면 가져오기

import retro
import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
import numpy as np

#게임 환경 생성
env = retro.make(game='SuperMarioBros-Nes', state='Level2-1')
#새 게임 시작
env.reset()

#화면 가져오기
screen = env.get_screen()   #RGB값이 담겨있는 픽셀파일

# print(screen.shape) #마지막에 출력되는 3은 dimension이고 RGB값이기에 RGB가 된다.

# print(screen)

class MyApp(QWidget):
    # GUI 창 속에 띄울 요소 - QWidget을 베이스로하는 껍데기 만든 것
    # Class는 붕어빵과 붕어빵틀 중에 붕어빵틀에 해당이 됨
    def __init__(self):     #초기화자, 생성자 역할을 한다고 생각하면 됨
        super().__init__()  #C/C++에서 #include부터 return 0까지하는 거라고 보면 됨

        # 이미지도 QLabel로 띄울 수 있음
        label_image = QLabel(self)
        global screen
        image = screen
        a = image.shape[1], image.shape[0]
        b = 1.5
        c = (a[0]*b, a[1]*b)
        qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)        #shape 1번지 = 높이값, 0번지 = 너비값, RGB888
        # qimage = QImage(image, c[0], c[1], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        # pixmap = pixmap.scaled(self.c[1], self.c[0], Qt.IgnoreAspectRatio)      #원본데이터 무시하고 100*100으로 바꿔라, 마리오 게임화면의 스케일을 키우는데 사용할 예정
        pixmap = pixmap.scaled(c[0], c[1], Qt.IgnoreAspectRatio)

        label_image.setPixmap(pixmap)
        label_image.setGeometry(0, 0, c[0], c[1])

        self.setFixedSize(c[0], c[1])
        self.setWindowTitle('GA Mario')

        self.show()         #창 띄우기


if __name__ == '__main__':   #여기에 적는 코드들은 직접 실행할 때만 실행가능, 외부에서 불러올 경우 여기에 포함된 코드는 실행되지 않음
    app = QApplication(sys.argv)
    window = MyApp()        # 붕어빵을 찍어내는 것, 붕어빵 이름이 window
    sys.exit(app.exec())    #여기까지 거의 고정적으로 쓰는 코드들들

