# 06. get_full_screen_tile.py

import retro
import sys
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
import numpy as np

env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
env.reset()

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

        self.setFixedSize(600, 300)

        self.setWindowTitle('GA Mario')
        global full_screen_tiles
        global ram
        global screen_tiles
        self.full_screen_tiles = full_screen_tiles
        self.screen_tiles = screen_tiles

        self.show()

    # 창이 업데이트 될 때마다 실행되는 함수
    def paintEvent(self, event):
        # 그리기 도구
        painter = QPainter()
        # 그리기 시작
        painter.begin(self)

        painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))
        ccnt = 1
        # for i in self.full_screen_tiles:
        for i in self.screen_tiles:
            cnt=-1
            for j in i:
                cnt+=1
                if j == 0:
                    # RGB 색상으로 브러쉬 설정
                    painter.setBrush(Qt.gray)
                    painter.drawRect(cnt*16, ccnt*16, 16, 16)
                else :
                    painter.setBrush(Qt.cyan)
                    painter.drawRect(cnt*16, ccnt*16, 16, 16)
            ccnt += 1
        painter.end()


    def timer(self):
        self.env.step(self.press_button)       #버튼정보 보내기
        self.screen = self.env.get_screen()    #화면에 뿌려줌
        self.image = self.screen               #image 함수에 적용

        self.full_screen_tiles = ram[0x0500:0x069F+1]

        self.full_screen_tile_count = self.full_screen_tiles.shape[0]

        self.full_screen_page1_tile = self.full_screen_tiles[:self.full_screen_tile_count//2].reshape((13, 16))
        self.full_screen_page2_tile = self.full_screen_tiles[self.full_screen_tile_count//2:].reshape((13, 16))

        self.full_screen_tiles = np.concatenate((self.full_screen_page1_tile, self.full_screen_page2_tile), axis=1).astype(np.int)
        # 0x071A	Current screen (in level)
        # 현재 화면이 속한 페이지 번호
        self.current_screen_page = ram[0x071A]
        # 0x071C	ScreenEdge X-Position, loads next screen when player past it?
        # 페이지 속 현재 화면 위치
        self.screen_position = ram[0x071C]
        # 화면 오프셋
        self.screen_offset = (256 * self.current_screen_page + self.screen_position) % 512
        # 타일 화면 오프셋
        self.screen_tile_offset = self.screen_offset // 16
        # 현재 화면 추출
        self.screen_tiles = np.concatenate((self.full_screen_tiles, self.full_screen_tiles), axis=1)[:, self.screen_tile_offset:self.screen_tile_offset+16]





        a = self.image.shape[1], self.image.shape[0]
        b = 3

        self.c = (a[0] * b, a[1] * b)
        self.qimage = QImage(self.image, self.image.shape[1], self.image.shape[0],
                             QImage.Format_RGB888)  # shape 1번지 = 높이값, 0번지 = 너비값, RGB888

        self.pixmap = QPixmap(self.qimage)

        self.pixmap = self.pixmap.scaled(self.c[0], self.c[1], Qt.IgnoreAspectRatio)    #스케일

        self.label_image.setPixmap(self.pixmap)
        # self.label_image.setGeometry(0, 0, self.c[0], self.c[1])

        # self.setFixedSize(self.c[0], self.c[1])
        # self.setWindowTitle('GA Mario')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())



