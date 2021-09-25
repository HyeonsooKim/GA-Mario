import retro
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
import numpy as np
import random
import os

#Activation 함수(ReLU, Sigmoid함수 정의)
#def 함수정의와 같은 방식임 단지 lambda를 사용하면서 한줄로 함수를 표현할 수 있는 거임(활용도 높으니 다양한 응용사례를 접해볼 것)
relu = lambda x: np.maximum(0, x)
sigmoid = lambda x: 1.0 / (1.0 + np.exp(-x))

class Chromosome:
    def __init__(self):
        #유전 정보(저장할 예정)

        #80(Input) to 9(hidden)
        self.w1 = np.random.uniform(low=-1, high=1, size=(80, 9))
        self.b1 = np.random.uniform(low=-1, high=1, size=(9,))

        #9(hidden) to 6(output)
        self.w2 = np.random.uniform(low=-1, high=1, size=(9, 6))
        self.b2 = np.random.uniform(low=-1, high=1, size=(6,))

        self.distance = 0
        self.max_distance = 0
        self.frames = 0
        self.stop_frames = 0
        self.win = 0

    #예측
    def predict(self, data):
        l1 = relu(np.matmul(data, self.w1) + self.b1)
        output = sigmoid(np.matmul(l1, self.w2) + self.b2)
        result = (output > 0.5).astype(np.int)
        return result

    #거리를 적합도로 사용
    def fitness(self):
        # # 1. 시간을 반영한 거리 점수(지수함수 반영해서 둘의 차이가 점점 더 벌어질 수 있도록)
        # fit = self.distance ** 1.8 - self.frames ** 1.5
        #
        # # 2. 조금이라도 움직인 경우 보너스
        # # if self.distance>50:
        # #     fit+=2500
        # # 같은 식
        # fit += min(max(self.distance-50, 0), 1) * 2500
        #
        # # 3. 목적지에 도달한 경우 보너스 +1 000 000
        # fit == self.win * 1000000
        #
        # # 4. 아무리 못해도 기본점수 1점
        # fit = max(fit, 1)
        #
        # # return self.distance
        # return int(fit)

        return int(max(self.distance**1.8 - self.frames**1.5+min(max(self.distance-50, 0), 1) * 2500 + self.win * 1000000, 1))

#유전 알고리즘
class GeneticAlgorithm:
    def __init__(self):
        #초기 크로모송 모델 10개
        self.chromosomes = [Chromosome() for _ in range(10)]
        #0번째 세대에서 시작
        self.generation = 0
        self.current_chromosome_index = 0

    #룰렛휠 선택
    def roulette_wheel_selection(self):
        #결과
        result = []
        # fitness_sum = sum(c.fitness() for c in chromosomes)
        #적합도의 합
        fitness_sum = 0
        #각 적합도의 총합
        for chromosome in self.chromosomes:
            fitness_sum += chromosome.fitness()
        #2회 실행
        for _ in range(2):
            #0부터 총합까지 랜덤한 숫자를 뽑음
            pick = random.uniform(0, fitness_sum)
            current = 0
            #룰렛을 Flatten 시 pick이 가르키는위치가 몇 번째인지 알기 위해 current에 기존의 section?을 더함 current가 더해지면서 pick을 넘어가는 그 순간 더해진 section이 선택되는 거임
            for chromosome in self.chromosomes:
                current += chromosome.fitness()
                if current > pick:
                    result.append(chromosome)
                    break
        return result

    def elitist_preserve_selection(self):
        sorted_chromosomes = sorted(self.chromosomes, key=lambda x: x.fitness(), reverse=True)
        return sorted_chromosomes[:2]

    def selection(self):
        result = self.roulette_wheel_selection()
        return result

    def simulated_binary_crossover(self, parent_chromosome1, parent_chromosome2):
        rand = np.random.random(parent_chromosome1.shape)
        gamma = np.empty(parent_chromosome1.shape)
        gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (100 + 1))
        gamma[rand > 0.5] = (2 * rand[rand > 0.5]) ** (1.0 / (100 + 1))
        child_chromosome1 = 0.5 * ((1 + gamma) * parent_chromosome1 + (1 - gamma) * parent_chromosome2)
        child_chromosome2 = 0.5 * ((1 - gamma) * parent_chromosome1 + (1 + gamma) * parent_chromosome2)
        return child_chromosome1, child_chromosome2

    def crossover(self, chromosome1, chromosome2):
        child1 = Chromosome()
        child2 = Chromosome()

        child1.w1, child2.w1 = self.simulated_binary_crossover(chromosome1.w1, chromosome2.w1)
        child1.b1, child2.b1 = self.simulated_binary_crossover(chromosome1.b1, chromosome2.b1)
        child1.w2, child2.w2 = self.simulated_binary_crossover(chromosome1.w2, chromosome2.w2)
        child1.b2, child2.b2 = self.simulated_binary_crossover(chromosome1.b2, chromosome2.b2)

        return child1, child2

    #각각의 랜덤값을 뽑아서 5%확률로 변이가 일어나는 것
    def static_mutation(self, chromosome):
        mutation_array = np.random.random(chromosome.shape) < 0.05
        gaussian_mutation = np.random.normal(size=chromosome.shape)
        chromosome[mutation_array] += gaussian_mutation[mutation_array]

    def mutation(self, chromosome):
        self.static_mutation(chromosome.w1)
        self.static_mutation(chromosome.b1)
        self.static_mutation(chromosome.w2)
        self.static_mutation(chromosome.b2)

    def next_generation(self):
        #파일은 없으면 자동생성 하지만 폴더는 자동생성하지 않음/ import os 추가한 뒤 사용
        if not os.path.exists('../data'):
            os.mkdir('../data')
        if not os.path.exists(f'../data/{self.generation}'):
            os.mkdir(f'../data/{self.generation}')

        #저장 기능 추가
        for i in range(10):
            if not os.path.exists(f'../data/{self.generation}/{i}'):
                os.mkdir(f'../data/{self.generation}/{i}')

            np.save(f'../data/{self.generation}/{i}/w1.npy', self.chromosomes[i].w1)
            np.save(f'../data/{self.generation}/{i}/b1.npy', self.chromosomes[i].b1)
            np.save(f'../data/{self.generation}/{i}/w2.npy', self.chromosomes[i].w2)
            np.save(f'../data/{self.generation}/{i}/b2.npy', self.chromosomes[i].b2)


        print(f'{self.generation}세대 시뮬레이션 완료.')

        next_chromosomes = []
        #엘리트 보존은 바로 다음 세대로 넘어감(20%)
        next_chromosomes.extend(self.elitist_preserve_selection())
        print(f'엘리트 적합도: {next_chromosomes[0].fitness()}')

        #4번 반복해서 2번씩(선택, 교배, 변이로 다음 구성원 채워감)
        for i in range(4):
            selected_chromosome = self.selection()

            child_chromosome1, child_chromosome2 = self.crossover(selected_chromosome[0], selected_chromosome[1])

            self.mutation(child_chromosome1)
            self.mutation(child_chromosome2)

            next_chromosomes.append(child_chromosome1)
            next_chromosomes.append(child_chromosome2)

        #세대 교체
        self.chromosomes = next_chromosomes
        #초기화
        for c in self.chromosomes:
            c.distance = 0
            c.max_distance = 0
            c.frames = 0
            c.stop_frames = 0
            c.win = 0

        self.generation += 1
        self.current_chromosome_index = 0


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # 창 제목 설정
        self.setWindowTitle('GA-Mario')

        self.env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        screen = self.env.reset()

        self.screen_width = screen.shape[0] * 2
        self.screen_height = screen.shape[1] * 2

        # 창 크기 고정
        self.setFixedSize(self.screen_width + 600, self.screen_height + 100)

        self.screen_label = QLabel(self)
        self.screen_label.setGeometry(0, 0, self.screen_width, self.screen_height)

        self.ga = GeneticAlgorithm()

        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game)
        self.game_timer.start(1000 // 60)

        # 창 띄우기
        self.show()

    def update_game(self):
        screen = self.env.get_screen()
        qimage = QImage(screen, screen.shape[1], screen.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(self.screen_width, self.screen_height, Qt.IgnoreAspectRatio)
        self.screen_label.setPixmap(pixmap)
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.setPen(QPen(Qt.black))

        ram = self.env.get_ram()

        full_screen_tiles = ram[0x0500:0x069F + 1]

        full_screen_tile_count = full_screen_tiles.shape[0]

        full_screen_page1_tile = full_screen_tiles[:full_screen_tile_count // 2].reshape((13, 16))
        full_screen_page2_tile = full_screen_tiles[full_screen_tile_count // 2:].reshape((13, 16))

        full_screen_tiles = np.concatenate((full_screen_page1_tile, full_screen_page2_tile), axis=1).astype(np.int)

        enemy_drawn = ram[0x000F:0x0013 + 1]

        enemy_horizon_position = ram[0x006E:0x0072 + 1]
        enemy_screen_position_x = ram[0x0087:0x008B + 1]
        enemy_position_y = ram[0x00CF:0x00D3 + 1]
        enemy_position_x = (enemy_horizon_position * 256 + enemy_screen_position_x) % 512

        enemy_tile_position_x = (enemy_position_x + 8) // 16
        enemy_tile_position_y = (enemy_position_y - 8) // 16 - 1

        for i in range(5):
            if enemy_drawn[i] == 1:
                ey = enemy_tile_position_y[i]
                ex = enemy_tile_position_x[i]
                if 0 <= ex < full_screen_tiles.shape[1] and 0 <= ey < full_screen_tiles.shape[0]:
                    full_screen_tiles[ey][ex] = -1

        current_screen_page = ram[0x071A]
        screen_position = ram[0x071C]
        screen_offset = (256 * current_screen_page + screen_position) % 512
        screen_tile_offset = screen_offset // 16

        screen_tiles = np.concatenate((full_screen_tiles, full_screen_tiles), axis=1)[:, screen_tile_offset:screen_tile_offset + 16]

        for i in range(screen_tiles.shape[0]):
            for j in range(screen_tiles.shape[1]):
                if screen_tiles[i][j] > 0:
                    screen_tiles[i][j] = 1
                    painter.setBrush(QBrush(Qt.cyan))
                elif screen_tiles[i][j] == -1:
                    screen_tiles[i][j] = 2
                    painter.setBrush(QBrush(Qt.red))
                else:
                    painter.setBrush(QBrush(Qt.gray))
                painter.drawRect(self.screen_width + 16 * j, 16 * i, 16, 16)

        player_position_x = ram[0x03AD]
        player_position_y = ram[0x03B8]

        player_tile_position_x = (player_position_x + 8) // 16
        player_tile_position_y = (player_position_y + 8) // 16 - 1

        painter.setBrush(QBrush(Qt.blue))
        painter.drawRect(self.screen_width + 16 * player_tile_position_x, 16 * player_tile_position_y, 16, 16)

        painter.setPen(QPen(Qt.magenta, 4, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)
        frame_x = player_tile_position_x
        frame_y = 2
        painter.drawRect(self.screen_width + 16 * frame_x, 16 * frame_y, 16 * 8, 16 * 10)

        input_data = screen_tiles[frame_y:frame_y+10, frame_x:frame_x+8]

        if 2 <= player_tile_position_y <= 11:
            input_data[player_tile_position_y - 2][0] = 2

        input_data = input_data.flatten()

        current_chromosome = self.ga.chromosomes[self.ga.current_chromosome_index]
        current_chromosome.frames += 1

        player_horizon_position = ram[0x006D]
        player_screen_position_x = ram[0x0086]
        current_chromosome.distance = 256 * player_horizon_position + player_screen_position_x

        if current_chromosome.max_distance < current_chromosome.distance:
            current_chromosome.max_distance = current_chromosome.distance
            current_chromosome.stop_frames = 0
        else:
            current_chromosome.stop_frames += 1

        player_float_state = ram[0x001D]
        player_state = ram[0x000E]
        player_vertical_screen_position = ram[0x00B5]

        if player_float_state == 0x03 or player_state in (0x06, 0x0B) or player_vertical_screen_position >= 2 or current_chromosome.stop_frames > 180:
            if player_float_state == 0x03:
                current_chromosome.win = 1

            print(f'{self.ga.current_chromosome_index + 1}번 마리오: {current_chromosome.fitness()}')

            self.ga.current_chromosome_index += 1

            if self.ga.current_chromosome_index == 10:
                self.ga.next_generation()
                print(f'== {self.ga.generation} 세대 ==')

            self.env.reset()
        else:
            predict = current_chromosome.predict(input_data)
            press_buttons = np.array([predict[5], 0, 0, 0, predict[0], predict[1], predict[2], predict[3], predict[4]])
            self.env.step(press_buttons)

            for i in range(predict.shape[0]):
                if predict[i] == 1:
                    painter.setBrush(QBrush(Qt.magenta))
                else:
                    painter.setBrush(QBrush(Qt.gray))
                painter.drawEllipse(self.screen_width + i * 40, 450, 10 * 2, 10 * 2)
                text = ('U', 'D', 'L', 'R', 'A', 'B')[i]
                painter.drawText(self.screen_width + i * 40, 480, text)


        painter.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())