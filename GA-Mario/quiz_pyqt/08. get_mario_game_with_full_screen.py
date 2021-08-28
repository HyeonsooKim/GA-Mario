# 08. get_mario_game_with_full_screen.py

# [도전과제8]
# 06. get_full_screen_tile.py 에서 가져온 전체 타일 정보를 그리기

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
        global ram

        #화면 갱신
        self.ram = ram
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

        self.setFixedSize(self.c[0]+600, self.c[1])
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

    # full screen
    def paintEvent(self, event):
        # 그리기 도구
        self.painter = QPainter()
        # -------------------------내 포지션-----------------------------------------------------------------------
        # 0x03AD	Player x pos within current screen offset
        # 현재 화면 속 플레이어 x 좌표
        self.player_position_x = self.ram[0x03AD]
        # 0x03B8	Player y pos within current screen
        # 현재 화면 속 플레이어 y 좌표
        self.player_position_y = self.ram[0x03B8]

        # 타일 좌표로 변환
        self.player_tile_position_x = (self.player_position_x + 8) // 16
        self.player_tile_position_y = (self.player_position_y + 8) // 16 - 1
        # -------------------------스크린-------------------------------------------------------------------------
        self.full_screen_tiles = self.ram[0x0500:0x069F + 1]

        self.full_screen_tile_count = self.full_screen_tiles.shape[0]

        self.full_screen_page1_tile = self.full_screen_tiles[:self.full_screen_tile_count // 2].reshape((13, 16))
        self.full_screen_page2_tile = self.full_screen_tiles[self.full_screen_tile_count // 2:].reshape((13, 16))

        self.full_screen_tiles = np.concatenate((self.full_screen_page1_tile, self.full_screen_page2_tile),
                                                axis=1).astype(np.int)

        # -------------------------------------------그리기 시작--------------------------------------------------------
        # 그리기 시작
        self.painter.begin(self)

        self.painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))
        ccnt = 1
        for i in self.full_screen_tiles:
            cnt = -1
            for j in i:
                cnt += 1
                if j == 0:
                    self.painter.setBrush(Qt.gray)
                    self.painter.drawRect(self.c[0] + cnt * 16, ccnt * 16 - 16, 16, 16)
                    # print(self.player_tile_position_y )   #1-13

                elif j < 0:
                    self.painter.setBrush(Qt.red)
                    self.painter.drawRect(self.c[0] + cnt * 16, ccnt * 16 - 16, 16, 16)

                else:
                    self.painter.setBrush(Qt.cyan)
                    self.painter.drawRect(self.c[0] + cnt * 16, ccnt * 16 - 16, 16, 16)

            ccnt += 1

        self.painter.end()

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

