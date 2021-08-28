# 07. get_mario_game_with_keyboard_control.py
# [도전과제7]
# 키보드로 조작할 수 있게 만들기
# 실행했을 때 코인이 깜빡이고 인게임 타이머가 동작하도록 만들기
# (1/60초마다 step 호출하고 화면 정보 QLabel에 다시 표시하기)
# 1/60 초마다 호출되는 함수 만들기 (lab-pyqt/05. pyqt_timer.py)
# 1/60 초마다 step함수 호출하기 (lab-mario/04. input_test.py)
# 1/60 초마다 화면 정보를 QLabel에 표시하기 (도전과제6)
# 키보드로 조작 가능하게 만들기
#
# [도전과제7 세부 가이드]
# 게임 화면 2배 크기로 창 크기 설정
# 창 제목: GA-Mario
# 조작 기능 없이 인게임 타이머가 작동하게 만들기
# 1/60초마다 아무것도 누르지 않은 키 정보 전송
# 변경된 게임 화면을 가져와서 화면에 표시
# 조작 기능 구현
# 팁: __init__() 함수에 눌린 키 정보를 담는 배열을 선언해서 활용
# (예시) self.press_buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0]
# 키보드가 눌리고 뗄 때 해당하는 키 정보 배열 값을 변경(0 <-> 1)
# 1/60초마다 위에서 만들어진 키 배열을 전송
# 게임 플레이 중 실행화면 자신 이름 칸에 업로드
# 작성한 코드 깃허브에 업로드

import sys
import retro
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

env = retro.make(game='SuperMarioBros-Nes', state='Level2-1')
env.reset()


#화면 가져오기
screen = env.get_screen()   #RGB값이 담겨있는 픽셀파일

ram = env.get_ram()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.label_image = QLabel(self)

        self.setWindowTitle('GA Mario')
        global env
        global screen

        #화면 갱신
        self.env = env
        self.press_button = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.image = screen

        self.a = self.image.shape[1], self.image.shape[0]
        self.b = 3
        self.c = (self.a[0] * self.b, self.a[1] * self.b)
        self.qimage = QImage(self.image, self.image.shape[1], self.image.shape[0],
                             QImage.Format_RGB888)  # shape 1번지 = 높이값, 0번지 = 너비값, RGB888

        self.pixmap = QPixmap(self.qimage)
        #원본데이터 무시하고 100*100으로 바꿔라, 마리오 게임화면의 스케일을 키우는데 사용할 예정
        self.pixmap = self.pixmap.scaled(self.c[0], self.c[1], Qt.IgnoreAspectRatio)

        self.label_image.setPixmap(self.pixmap)
        self.label_image.setGeometry(0, 0, self.c[0], self.c[1])
        # self.ram_map.setGeometry(self.c[0], self.c[1]-220, self.c[0]+512, self.c[1])

        self.setFixedSize(self.c[0], self.c[1])
        self.setWindowTitle('GA Mario')

        # 타이머 생성
        qtimer = QTimer(self)
        # 타이머에 실행할 함수 연결
        qtimer.timeout.connect(self.timer)
        # 0.01667초마다 연결된 함수를 실행
        qtimer.start(16.667)
        # self.cnt = 0
        self.show()

    def timer(self):
        self.env.step(self.press_button)       #버튼정보 보내기
        self.screen = self.env.get_screen()    #화면에 뿌려줌
        self.image = self.screen               #image 함수에 적용
        self.ram = self.env.get_ram()

#------------------------------------------------화면 표시-------------------------------------------------------
        self.qimage = QImage(self.image, self.image.shape[1], self.image.shape[0],
                             QImage.Format_RGB888)  # shape 1번지 = 높이값, 0번지 = 너비값, RGB888

        self.pixmap = QPixmap(self.qimage)

        self.pixmap = self.pixmap.scaled(self.c[0], self.c[1], Qt.IgnoreAspectRatio)    #스케일

        self.label_image.setPixmap(self.pixmap)

        self.update()

        #키를 누를 때
    def keyPressEvent(self, event):
        key = event.key()

        # 키 배열: B, NULL, SELECT, START, U, D, L, R, A
        if key == Qt.Key_A:
            print('A key')
            self.press_button[8] = 1
        elif key == Qt.Key_S:
            print('B key')
            self.press_button[0] = 1
        elif key == Qt.Key_Up:
            print('Up key')
            self.press_button[4] = 1
        elif key == Qt.Key_Down:
            print('Down key')
            self.press_button[5] = 1
        elif key == Qt.Key_Left:
            print('Left key')
            self.press_button[6] = 1
        elif key == Qt.Key_Right:
            print('Right key')
            self.press_button[7] = 1
        elif key == Qt.Key_Enter:
            print('Enter key')
            self.press_button[2] = 1
        elif key == Qt.Key_Space:
            print('Space key')
            self.press_button[3] = 1

    #키를 뗄 때
    def keyReleaseEvent(self, event):
        key = event.key()
        if key == Qt.Key_A:
            print('A key')
            self.press_button[8] = 0
        elif key == Qt.Key_S:
            print('B key')
            self.press_button[0] = 0
        elif key == Qt.Key_Up:
            print('Up key')
            self.press_button[4] = 0
        elif key == Qt.Key_Down:
            print('Down key')
            self.press_button[5] = 0
        elif key == Qt.Key_Left:
            print('Left key')
            self.press_button[6] = 0
        elif key == Qt.Key_Right:
            print('Right key')
            self.press_button[7] = 0
        elif key == Qt.Key_Enter:
            print('Enter key')
            self.press_button[2] = 0
        elif key == Qt.Key_Space:
            print('Space key')
            self.press_button[3] = 0
        # self.press_button = np.empty(9)
        # self.press_button.fill(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())





