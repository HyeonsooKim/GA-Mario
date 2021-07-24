# 04. input_test.py
# 게임에 입력 보내기
import sys
import retro
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

#게임 환경 생성
env = retro.make(game='SuperMarioBros-Nes', state='Level2-1')
#새 게임 시작
env.reset()

#키 배열: B, NULL, SELECT, START, U, D, L, R, A
env.step(np.array([0, 0, 0, 0, 0, 0, 0, 0]))        #입력을 보내는 기능이 이게 끝임, 전용 게임기에 있는 키값들을 하나의 배열로 만드는 것
# 스텝이라는 함수를 쓰지 않으면 멈춰있고 프레임마다 호출됨
# 60프레임이면 1/60초마다 호출되게 만드는데 이때 pyqt의 timer를 사용
