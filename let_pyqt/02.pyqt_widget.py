#02. pyqt.widget.py
#PyQt5 위젯
import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
import numpy as np

class MyApp(QWidget):
    # GUI 창 속에 띄울 요소 - QWidget을 베이스로하는 껍데기 만든 것
    # Class는 붕어빵과 붕어빵틀 중에 붕어빵틀에 해당이 됨
    def __init__(self):     #초기화자, 생성자 역할을 한다고 생각하면 됨
        super().__init__()  #C/C++에서 #include부터 return 0까지하는 거라고 보면 됨

        # 창 크기 고정, self는 나!
        self.setFixedSize(400, 300)

        # 창 제목
        self.setWindowTitle('GA Mario')

        # 버튼 만들기
        button = QPushButton(self)
        button.setText('Button_for_nextop')                  #버튼 이름
        button.setGeometry(100, 100, 200, 20)               #위치, 너비, 높이 입력

        # 텍스트 삽입하기
        label_text = QLabel(self)
        label_text.setText('Nextop')        #텍스트 이름 정하기
        label_text.setGeometry(200, 200, 50, 100)                 #텍스트 위치, 너비, 높이 입력

        # 이미지도 QLabel로 띄울 수 있음
        label_image = QLabel(self)

        image = np.array([[[10, 10, 10], [10, 10, 10]], [[0, 0, 0], [0, 0, 0]]]) #2x2 흰색픽셀로 된 정사각형 이미지
        qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)        #shape 1번지 = 높이값, 0번지 = 너비값, RGB888
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(100, 100, Qt.IgnoreAspectRatio)

        label_image.setPixmap(pixmap)
        label_image.setGeometry(0, 0, 100, 100)

        self.show()         #창 띄우기


if __name__ == '__main__':   #여기에 적는 코드들은 직접 실행할 때만 실행가능, 외부에서 불러올 경우 여기에 포함된 코드는 실행되지 않음
    app = QApplication(sys.argv)
    window = MyApp()        # 붕어빵을 찍어내는 것, 붕어빵 이름이 window
    sys.exit(app.exec())    #여기까지 거의 고정적으로 쓰는 코드들들