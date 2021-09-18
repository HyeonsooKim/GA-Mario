# 07.roulette_wheel_selection.py

import numpy as np
import random

relu = lambda x: np.maximum(0, x)
sigmoid = lambda x: 1.0 / (1.0 + np.exp(-x))


class Chromosome:
    def __init__(self):
        self.w1 = np.random.uniform(low=-1, high=1, size=(13 * 16, 9))
        self.b1 = np.random.uniform(low=-1, high=1, size=(9,))

        self.w2 = np.random.uniform(low=-1, high=1, size=(9, 6))
        self.b2 = np.random.uniform(low=-1, high=1, size=(6,))

        self.distance = int(random.uniform(1,100))
        self.max_distance = 0
        self.frames = 0
        self.stop_frames = 0
        self.win = 0

    def predict(self, data):
        l1 = relu(np.matmul(data, self.w1) + self.b1)
        output = sigmoid(np.matmul(l1, self.w2) + self.b2)
        result = (output > 0.5).astype(np.int)
        return result

    def fitness(self):
        return self.distance

def roulette_sheel_selection(chromosomes):
    #룰렛판을 만들어서 적합도의 비중을 가지고 각각의 영역을 어떻게 차지하게 하느냐
    result = []
    fitness_sum = 0
    for chromosome in chromosomes:
        fitness_sum += chromosome.fitness()

    for _ in range(2):  #2번하고 싶다면
        pick = random.uniform(0, fitness_sum) #정규분포로 0에서 fitness_sum까지의 값을 뽑음
        current = 0
        for chromosome in chromosomes:
            current += chromosome.fitness()
            if current > pick:
                result.append(chromosome)
                break

    return result

if __name__ == '__main__':
    n = 3
    #테스트 코드----
    chromosomes = [Chromosome() for _ in range(10)] #10개 뽑음
    selected_chromosome = roulette_sheel_selection(chromosomes)
    print(selected_chromosome)
    for c in chromosomes:
        print(c.fitness(), end=' ')
    print()
    print('==선택된 염색체의 적합도==')
    print(selected_chromosome[0].fitness(), selected_chromosome[1].fitness())
    #----------------------------------------
    model = Chromosome()
    data = np.random.randint(0, 3, (13 * 16,), dtype=np.int)