#14. my_fitness_fomula_with_fitness.py
# [도전과제14]
# 05. fitness.py 에 적합도 기준을 참고해서 나만의 적합도 식 만들어보기 (def fitness 함수 만들기)

def fitness(self):

    # 재료: 이동거리, 시간(프레임), 클리어
    distance = 0
    frames = 0
    win = 0

    # 적합도 기준
    # 1. 많은 거리를 이동했다면 높은 적합도
    # 2. 같은 거리라도 더 짧은 시간에 도달했다면 높은 적합도
    # 3. 클리어한 AI는 가장 높은 적합도

    # 1.
    fitness = distance^3

    # 2.
    fitness = distance - frames^4

    # 3.
    fitness += win * 1000000