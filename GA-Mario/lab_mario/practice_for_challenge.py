# 04. input_test.py
# 게임에 입력 보내기
import sys
import retro
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

#게임 환경 생성
env = retro.make(game='SuperMarioBros-Nes', state='Level5-1')

#새 게임 시작
env.reset()

#키 배열: B, NULL, SELECT, START, U, D, L, R, A
# env.step(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]))        #입력을 보내는 기능이 이게 끝임, 전용 게임기에 있는 키값들을 하나의 배열로 만드는 것
# 스텝이라는 함수를 쓰지 않으면 멈춰있고 프레임마다 호출됨
# 60프레임이면 1/60초마다 호출되게 만드는데 이때 pyqt의 timer를 사용

#화면 가져오기
screen = env.get_screen()   #RGB값이 담겨있는 픽셀파일

ram = env.get_ram()

class MyApp(QWidget):
    def __init__(self):  # 초기화자, 생성자 역할을 한다고 생각하면 됨
        super().__init__()  # C/C++에서 #include부터 return 0까지하는 거라고 보면 됨

        # 이미지도 QLabel로 띄울 수 있음
        self.label_image = QLabel(self)
        self.ram_map = QLabel(self)

        # global full_screen_tiles
        global env
        global screen
        global ram
        # global screen_tiles

        #화면 갱신
        self.env = env
        self.screen = screen
        self.press_button = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.image = self.screen

        #현재 및 전체 화면
        # self.full_screen_tiles = full_screen_tiles
        # self.screen_tiles = screen_tiles

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
        self.ram_map.setGeometry(self.c[0], self.c[1]-220, self.c[0]+512, self.c[1])

        self.setFixedSize(self.c[0]+600, self.c[1])
        self.setWindowTitle('GA Mario')

        # 타이머 생성
        qtimer = QTimer(self)
        # 타이머에 실행할 함수 연결
        qtimer.timeout.connect(self.timer)

        # 0.01667초마다 연결된 함수를 실행
        qtimer.start(16.667)

        self.show()  # 창 띄우기


    def timer(self):
        self.env.step(self.press_button)       #버튼정보 보내기
        self.screen = self.env.get_screen()    #화면에 뿌려줌
        self.image = self.screen               #image 함수에 적용

        a = self.image.shape[1], self.image.shape[0]
        b = 3

        self.c = (a[0] * b, a[1] * b)
        self.qimage = QImage(self.image, self.image.shape[1], self.image.shape[0],
                             QImage.Format_RGB888)  # shape 1번지 = 높이값, 0번지 = 너비값, RGB888

        self.pixmap = QPixmap(self.qimage)

        self.pixmap = self.pixmap.scaled(self.c[0], self.c[1], Qt.IgnoreAspectRatio)    #스케일

        self.label_image.setPixmap(self.pixmap)
        #-----------------------------------------------------------------------ram map-----------------------
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
    #                 self.painter.drawRect(self.c[0]+cnt*16, ccnt*16, 16, 16)
    #             else :
    #                 self.painter.setBrush(Qt.cyan)
    #                 self.painter.drawRect(self.c[0]+cnt*16, ccnt*16, 16, 16)
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