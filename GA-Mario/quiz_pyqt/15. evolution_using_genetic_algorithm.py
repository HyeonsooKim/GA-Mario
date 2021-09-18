#15. evolution_using_genetic_algorithm.py
# [도전과제15]
# 06. genetic_algorithm.py 에서 만든 유전 알고리즘을 이용해서 진화 시뮬레이션 구현하기

#12. play_game_with_chromosomes.py
# [도전과제13]
# 04. chromosomes.py 에서 만든 염색체로 마리오 게임 플레이하고 [도전과제12] 실행 속도 비교하기


import sys
import retro
import numpy as np
import tensorflow as tf
import random
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

# env = retro.make(game='SuperMarioBros-Nes', state='Level2-1')
# env.reset()
#
#
# #화면 가져오기
# screen = env.get_screen()   #RGB값이 담겨있는 픽셀파일
#
# ram = env.get_ram()

relu = lambda x: np.maximum(0, x)
sigmoid = lambda x: 1.0 / (1.0 + np.exp(-x))


class Chromosome:
    def __init__(self):
        self.w1 = np.random.uniform(low=-1, high=1, size=(13 * 16, 9))
        self.b1 = np.random.uniform(low=-1, high=1, size=(9,))

        self.w2 = np.random.uniform(low=-1, high=1, size=(9, 6))
        self.b2 = np.random.uniform(low=-1, high=1, size=(6,))

        self.distance = 0
        self.max_distance = 0
        self.frames = 0
        self.stop_frames = 0
        self.win = 0

    def predict(self, data):
        l1 = relu(np.matmul(data, self.w1) + self.b1)
        output = sigmoid(np.matmul(l1, self.w2) + self.b2)
        result = (output > 0.5).astype(np.int)
        return result


class Genetic_Algorithm:
    def roulette_wheel_selection(self, chromosomes):
        result = []
        # fitness_sum = sum(c.fitness() for c in chromosomes)
        fitness_sum = 0
        for chromosome in chromosomes:
            fitness_sum += chromosome.fitness()
        for _ in range(2):
            pick = random.uniform(0, fitness_sum)
            current = 0
            for chromosome in chromosomes:
                current += chromosome.fitness()
                if current > pick:
                    result.append(chromosome)
                    break
        return result

    def elitist_preserve_selection(self, chromosomes):
        # 상위 n개를 보존하는 것은 자유
        sorted_chromosomes = sorted(chromosomes, key=lambda x: x.fitness(), reverse=True)
        return sorted_chromosomes[:2]

    def static_mutation(self, chromosome):
        mutation_array = np.random.random(chromosome.shape) < 0.05
        gaussian_mutation = np.random.normal(size=chromosome.shape)
        chromosome[mutation_array] += gaussian_mutation[mutation_array]


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.label_image = QLabel(self)

        self.setWindowTitle('GA Mario')
        global env
        global screen
        global ram

        #유전 알고리즘
        # 순차적인 흐름을 만들어내는 모델을 만듦
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(9, input_shape=(13 * 16,), activation='relu'),
            tf.keras.layers.Dense(6, activation='sigmoid')
        ])

        #화면 갱신
        self.env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        self.ram = self.env.get_ram()
        self.env.reset()
        self.press_button = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.image = self.env.get_screen()

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
        self.update_game()

        # self.genetic_algorithm()

        # self.update()

    def genetic_algorithm(self):
        self.data = np.random.randint(0, 3, (13 * 16,), dtype=np.int)
        # print(self.data)

        self.predict = self.model.predict(np.array([self.data]))[0]
        # print(self.predict)

        self.result = (self.predict > 0.5).astype(np.int)
        self.press_button[8] = self.result[0]
        for bb in range(1, 5):
            self.press_button[bb + 3] = self.result[bb]
        # print(result)

    def update_screen(self):
        self.screen = self.env.get_screen()  # 화면에 뿌려줌
        self.image = self.screen  # image 함수에 적용
        self.ram = self.env.get_ram()

        # ------------------------------------------------화면 표시-------------------------------------------------------
        self.qimage = QImage(self.image, self.image.shape[1], self.image.shape[0],
                             QImage.Format_RGB888)  # shape 1번지 = 높이값, 0번지 = 너비값, RGB888

        self.pixmap = QPixmap(self.qimage)

        self.pixmap = self.pixmap.scaled(self.c[0], self.c[1], Qt.IgnoreAspectRatio)  # 스케일

        self.label_image.setPixmap(self.pixmap)

        self.update()

    def update_game(self):
        self.env.step(self.press_button)
        self.update_screen()
        # -------------------------------------------------get_status추가------------------------------------------------
        #   0x001D Player "float" state
        # 0x03 - 클리어
        self.player_float_state = self.ram[0x001D]
        print(self.player_float_state)

        if self.player_float_state == 0x03:
            print('클리어')

        # 0x000E	Player's state
        # 0x06, 0x0B - 게임 오버
        self.player_state = self.ram[0x000E]
        print(self.player_state)

        if self.player_state == 0x06 or self.player_state == 0x0B:
            self.env.reset()
            print('게임 오버 1')

        # 0x00B5	Player vertical screen position
        # anywhere below viewport is >1
        self.player_vertical_screen_position = self.ram[0x00B5]
        print(self.player_vertical_screen_position)

        if self.player_vertical_screen_position >= 2:
            self.env.reset()
            print('게임 오버 2')
        #---------------------------------------------------------------------------------------------------------------

    # full screen
    def paintEvent(self, event):
        # 그리기 도구
        self.painter = QPainter()
# -------------------------------------------내 포지션---------------------------------------------------------------
        # 0x03AD	Player x pos within current screen offset
        # 현재 화면 속 플레이어 x 좌표
        self.player_position_x = self.ram[0x03AD]
        # 0x03B8	Player y pos within current screen
        # 현재 화면 속 플레이어 y 좌표
        self.player_position_y = self.ram[0x03B8]

        # 타일 좌표로 변환
        self.player_tile_position_x = (self.player_position_x + 8) // 16
        self.player_tile_position_y = (self.player_position_y + 8) // 16 - 1
# ---------------------------------------------적 드로운------------------------------------------------------------
        # 0x000F-0x0013	Enemy drawn? Max 5 enemies at once.
        # 0 - No
        # 1 - Yes (not so much drawn as "active" or something)
        self.enemy_drawn = self.ram[0x000F:0x0013 + 1]

        loc = np.where(self.enemy_drawn == 1)[0]  # 1이되는 인덱스 반환해주는 함수
# -------------------------------------------적 포지션---------------------------------------------------------------
        # 0x006E-0x0072	Enemy horizontal position in level
        # 자신이 속한 화면 페이지 번호
        self.enemy_horizon_position = self.ram[0x006E:0x0072 + 1]
        # 0x0087-0x008B	Enemy x position on screen
        # 자신이 속한 페이지 속 x 좌표
        self.enemy_screen_position_x = self.ram[0x0087:0x008B + 1]
        # 0x00CF-0x00D3	Enemy y pos on screen
        self.enemy_position_y = self.ram[0x00CF:0x00D3 + 1]
        # 적 x 좌표
        self.enemy_position_x = (self.enemy_horizon_position * 256 + self.enemy_screen_position_x) % 512

        # 적 타일 좌표
        self.enemy_tile_position_x = (self.enemy_position_x + 8) // 16
        self.enemy_tile_position_y = (self.enemy_position_y - 8) // 16 - 1

        self.ene_x = self.enemy_tile_position_x[loc]  # 0~32
        self.ene_y = self.enemy_tile_position_y[loc]
# --------------------------------------------스크린-----------------------------------------------------------------
        self.full_screen_tiles = self.ram[0x0500:0x069F + 1]

        self.full_screen_tile_count = self.full_screen_tiles.shape[0]

        self.full_screen_page1_tile = self.full_screen_tiles[:self.full_screen_tile_count // 2].reshape((13, 16))
        self.full_screen_page2_tile = self.full_screen_tiles[self.full_screen_tile_count // 2:].reshape((13, 16))

        self.full_screen_tiles = np.concatenate((self.full_screen_page1_tile, self.full_screen_page2_tile),
                                                axis=1).astype(np.int)

        for a, b in zip(self.ene_x, self.ene_y):        #적 표시를 위함
            try:
                self.full_screen_tiles[b][a] = -1       #a가 0~32이므로 0~31만 여기 해당함
            except:
                continue                                #32일 때 skip
#--------------------------------------------현재 화면 표시-------------------------------------------------------------
        # 0x071A	Current screen (in level)
        # 현재 화면이 속한 페이지 번호
        self.current_screen_page = self.ram[0x071A]
        # 다음 화면이 속한 페이지 번호
        self.next_screen_page = self.ram[0x071B]
        # 0x071C	ScreenEdge X-Position, loads next screen when player past it?
        # 페이지 속 현재 화면 위치
        self.screen_position = self.ram[0x071C]
        # 화면 오프셋
        self.screen_offset = (256 * self.current_screen_page + self.screen_position) % 512
        # 타일 화면 오프셋
        self.screen_tile_offset = self.screen_offset // 16
        # 현재 화면 추출
        self.screen_tiles = np.concatenate((self.full_screen_tiles, self.full_screen_tiles), axis=1)[:,
                            self.screen_tile_offset:self.screen_tile_offset + 16]  # 16을 조절하면 그만큼 타일 수가 늘어남
        # 현재 풀스크린 추출
        self.screen_tiles_full = np.concatenate((self.full_screen_tiles, self.full_screen_tiles), axis=1)[:,
                                 self.screen_tile_offset:self.screen_tile_offset + 32]
        # -------------------------------------------그리기 시작--------------------------------------------------------
        # 그리기 시작
        self.painter.begin(self)

        self.painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))
        ccnt = 1
        # for i in range(screen_tiles.shape[0]):
        #   for j in range(screen_tiles.shape[1]);
        #     if screen_tiles[i][j] >0:
        #       screen_tiles[i][j] = 1
        #       painter.setbrush
        #     elif == -1:
        #         screen_tiles[i][j] = 2
        #         setbrush
        #     else:
        #         setbrush
        #     paint.drawRect(self.screen_width + 16 *j, 16*i, 16, 16)
        # 플레이어 위치
        # painter.drawRect(self.screen_width + 16 * player_tile_position_x, 16*player_tile_position_y, 16, 16)



        for i in self.screen_tiles_full:
            cnt = -1
            for j in i:
                cnt += 1
                if j == 0:
                    if ccnt - 1 == self.player_tile_position_y + 13 and cnt == self.player_tile_position_x:
                        self.painter.setBrush(Qt.blue)
                        self.painter.drawRect(self.c[0] + cnt * 16, ccnt * 16 + 200, 16, 16)
                    else:
                        self.painter.setBrush(Qt.gray)
                        self.painter.drawRect(self.c[0] + cnt * 16, ccnt * 16 - 16, 16, 16)
                elif j < 0:
                    self.painter.setBrush(Qt.red)
                    self.painter.drawRect(self.c[0] + cnt * 16, ccnt * 16 - 16, 16, 16)
                else:
                    self.painter.setBrush(Qt.cyan)
                    self.painter.drawRect(self.c[0] + cnt * 16, ccnt * 16 - 16, 16, 16)

            ccnt += 1

        for i in self.screen_tiles:
            cnt = -1
            for j in i:
                cnt += 1
                if j == 0:
                    # RGB 색상으로 브러쉬 설정
                    if ccnt - 1 == self.player_tile_position_y + 13 and cnt == self.player_tile_position_x:
                        self.painter.setBrush(Qt.blue)
                        self.painter.drawRect(self.c[0] + cnt * 16, ccnt * 16 + 200, 16, 16)
                        # print('check')
                    else:
                        self.painter.setBrush(Qt.gray)
                        self.painter.drawRect(self.c[0] + cnt * 16, ccnt * 16 + 200, 16, 16)
                        # print(ccnt) #14-24
                elif j < 0:
                    self.painter.setBrush(Qt.red)
                    self.painter.drawRect(self.c[0] + cnt * 16, ccnt * 16 + 200, 16, 16)
                else:
                    self.painter.setBrush(Qt.cyan)
                    self.painter.drawRect(self.c[0] + cnt * 16, ccnt * 16 + 200, 16, 16)
            ccnt += 1


        # 네모박스
        # frame_x = self.player_tile_position_x
        # frame_y = 2
        # self.painter.setBrush(Qt.NoBrush)
        # self.painter.setPen(QPen(Qt.magenta, 4, Qt.SolidLine))
        # # self.painter.drawRect(self.c[0], 16 * frame_x, 16 * frame_y, 16 * 8, 16 * 10)
        # self.painter.drawRect(self.c[0] + frame_x * 16, frame_y * 16 - 16, 16*8, 16*10)

        #제네틱

        input_data = input_data.flatten()
        current_chromosome = self.ga.chromosomes[self.ga.current_chromosome_index]
        current_chromosome.frames +=1

        current_chromosome.distance = 256 * player_horizon_position + player_screen_position_x

        if current_chromosome.max_distance < current_chromosome.distance:
            current_chromosome.max_distance=current_chromosome.distance
            current_chromosome.stop_frames = 0
        else:
            current_chromosome.stop_frames += 1
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
    #크로모솜
    ch_model = Chromosome()
    window.model = ch_model
    sys.exit(app.exec_())