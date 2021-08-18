# 06. get_full_screen_tile.py

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

# https://datacrystal.romhacking.net/wiki/Super_Mario_Bros.:RAM_map
# 0x0500-0x069F	Current tile (Does not effect graphics)
full_screen_tiles = ram[0x0500:0x069F+1]

full_screen_tile_count = full_screen_tiles.shape[0]

full_screen_page1_tile = full_screen_tiles[:full_screen_tile_count//2].reshape((13, 16))
full_screen_page2_tile = full_screen_tiles[full_screen_tile_count//2:].reshape((13, 16))

full_screen_tiles = np.concatenate((full_screen_page1_tile, full_screen_page2_tile), axis=1).astype(np.int)

current_screen_page = ram[0x071A]

screen_position = ram[0x071C]

screen_offset = (256 * current_screen_page + screen_position) % 512

screen_tile_offset = screen_offset // 16

screen_tiles = np.concatenate((full_screen_tiles, full_screen_tiles), axis=1)[:, screen_tile_offset:screen_tile_offset+16]

# sigmoid : 0~1의 확률값으로 바꿔줌

# Empty = 0x00
# Fake = 0x01
# Ground = 0x54
# Top_Pipe1 = 0x12
# Top_Pipe2 = 0x13
# Bottom_Pipe1 = 0x14
# Bottom_Pipe2 = 0x15
# Flagpole_Top =  0x24
# Flagpole = 0x25
# Coin_Block1 = 0xC0
# Coin_Block2 = 0xC1
# Coin = 0xC2
# Breakable_Block = 0x51



class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.label_image = QLabel(self)

        self.setWindowTitle('GA Mario')
        global full_screen_tiles
        global env
        global screen
        global ram
        global screen_tiles


        #화면 갱신
        self.env = env
        self.screen = screen
        self.press_button = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.image = self.screen

        self.ram = ram
        self.full_screen_tiles = full_screen_tiles
        self.screen_tiles = screen_tiles

        a = self.image.shape[1], self.image.shape[0]
        b = 3
        self.c = (a[0] * b, a[1] * b)
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
        self.cnt = 0
        self.show()

    def timer(self):
        self.env.step(self.press_button)       #버튼정보 보내기
        self.screen = self.env.get_screen()    #화면에 뿌려줌
        self.image = self.screen               #image 함수에 적용
        self.ram = self.env.get_ram()

#-------------------------------------------------------------플레이어 좌표--------------------------------
        # 0x03AD	Player x pos within current screen offset
        # 현재 화면 속 플레이어 x 좌표
        self.player_position_x = self.ram[0x03AD]
        # 0x03B8	Player y pos within current screen
        # 현재 화면 속 플레이어 y 좌표
        self.player_position_y = self.ram[0x03B8]

        # 타일 좌표로 변환
        self.player_tile_position_x = (self.player_position_x + 8) // 16
        self.player_tile_position_y = (self.player_position_y + 8) // 16 - 1

#-------------------------------------------------------------Enemy_Drawn--------------------------------
        # 0x000F-0x0013	Enemy drawn? Max 5 enemies at once.
        # 0 - No
        # 1 - Yes (not so much drawn as "active" or something)
        self.enemy_drawn = self.ram[0x000F:0x0013+1]

#-------------------------------------------------------------Enemy position----------------------------
        # 0x006E-0x0072	Enemy horizontal position in level
        # 자신이 속한 화면 페이지 번호
        self.enemy_horizon_position = self.ram[0x006E:0x0072+1]
        # 0x0087-0x008B	Enemy x position on screen
        # 자신이 속한 페이지 속 x 좌표
        self.enemy_screen_position_x = self.ram[0x0087:0x008B+1]
        # 0x00CF-0x00D3	Enemy y pos on screen
        self.enemy_position_y = self.ram[0x00CF:0x00D3+1]
        # 적 x 좌표
        self.enemy_position_x = (self.enemy_horizon_position * 256 + self.enemy_screen_position_x) % 512


        # 적 타일 좌표
        self.enemy_tile_position_x = (self.enemy_position_x + 8) // 16
        self.enemy_tile_position_y = (self.enemy_position_y - 8) // 16 - 1

#-------------------------------------------------------------

        a = self.image.shape[1], self.image.shape[0]
        b = 3

        self.c = (a[0] * b, a[1] * b)
        self.qimage = QImage(self.image, self.image.shape[1], self.image.shape[0],
                             QImage.Format_RGB888)  # shape 1번지 = 높이값, 0번지 = 너비값, RGB888

        self.pixmap = QPixmap(self.qimage)

        self.pixmap = self.pixmap.scaled(self.c[0], self.c[1], Qt.IgnoreAspectRatio)    #스케일

        self.label_image.setPixmap(self.pixmap)
        #-----------------------------------------------------------------------ram map-----------------------
        self.full_screen_tiles = self.ram[0x0500:0x069F+1]

        self.full_screen_tile_count = self.full_screen_tiles.shape[0]

        self.full_screen_page1_tile = self.full_screen_tiles[:self.full_screen_tile_count//2].reshape((13, 16))
        self.full_screen_page2_tile = self.full_screen_tiles[self.full_screen_tile_count//2:].reshape((13, 16))

        self.full_screen_tiles = np.concatenate((self.full_screen_page1_tile, self.full_screen_page2_tile), axis=1).astype(np.int)
        # 0x071A	Current screen (in level)
        # 현재 화면이 속한 페이지 번호
        self.current_screen_page = self.ram[0x071A]
        # 0x071C	ScreenEdge X-Position, loads next screen when player past it?
        # 페이지 속 현재 화면 위치
        self.screen_position = self.ram[0x071C]
        # 화면 오프셋
        self.screen_offset = (256 * self.current_screen_page + self.screen_position) % 512
        # 타일 화면 오프셋
        self.screen_tile_offset = self.screen_offset // 16
        # 현재 화면 추출
        self.screen_tiles = np.concatenate((self.full_screen_tiles, self.full_screen_tiles), axis=1)[:, self.screen_tile_offset:self.screen_tile_offset+16] #16을 조절하면 그만큼 타일 수가 늘어남

        #창을 새로고침
        self.update()

    # full screen
    def paintEvent(self, event):
        # 그리기 도구
        self.painter = QPainter()
        # 그리기 시작
        self.painter.begin(self)

        self.painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))
        ccnt = 1
        # for i in self.full_screen_tiles:
        for i in self.full_screen_tiles:
            cnt=-1
            for j in i:
                cnt+=1
                if j == 0:
                    # RGB 색상으로 브러쉬 설정
                    self.painter.setBrush(Qt.gray)
                    self.painter.drawRect(self.c[0]+cnt*16, ccnt*16-16, 16, 16)
                else :
                    self.painter.setBrush(Qt.cyan)
                    self.painter.drawRect(self.c[0]+cnt*16, ccnt*16-16, 16, 16)
            ccnt += 1

        for i in self.screen_tiles:
            cnt=-1
            for j in i:
                cnt+=1
                if j == 0:
                    # RGB 색상으로 브러쉬 설정
                    self.painter.setBrush(Qt.gray)
                    self.painter.drawRect(self.c[0]+cnt*16, ccnt*16+200, 16, 16)
                else :
                    self.painter.setBrush(Qt.cyan)
                    self.painter.drawRect(self.c[0]+cnt*16, ccnt*16+200, 16, 16)
            ccnt += 1
        self.painter.end()

    # current screen
    # def paintEvent(self, event):
    #     # 그리기 도구
    #     self.painter = QPainter()
    #     # 그리기 시작
    #     self.painter.begin(self)
    #
    #     self.painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))
    #     ccnt = 1
    #     # for i in self.full_screen_tiles:
    #     for i in self.screen_tiles:
    #         cnt=-1
    #         for j in i:
    #             cnt+=1
    #             if j == 0:
    #                 # RGB 색상으로 브러쉬 설정
    #                 self.painter.setBrush(Qt.gray)
    #                 self.painter.drawRect(self.c[0]+cnt*16, ccnt*16-10, 16, 16)
    #             else :
    #                 self.painter.setBrush(Qt.cyan)
    #                 self.painter.drawRect(self.c[0]+cnt*16, ccnt*16-10, 16, 16)
    #         ccnt += 1
    #     self.painter.end()



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




