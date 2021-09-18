# 08. elitist_preserve_selection.py

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

def elitist_preserve_selection(chromosomes):
    #상위 n개를 보존하는 것은 자유
    sorted_chromosomes = sorted(chromosomes, key=lambda x: x.fitness(), reverse=True)
    return sorted_chromosomes[:2]


if __name__=='__main__':
    chromosomes = [Chromosome() for _ in range(10)]
    elitiest_chromosome = elitist_preserve_selection(chromosomes)

    for c in chromosomes:
        print(c.fitness(), end=' ')
    print()
    print('==엘리트 염색체의 적합도==')
    print(elitiest_chromosome[0].fitness(), elitiest_chromosome[1].fitness())