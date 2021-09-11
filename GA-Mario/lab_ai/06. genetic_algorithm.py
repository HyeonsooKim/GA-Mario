# 06. genetic_algorithm.py
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

    def fitness(self):
        return self.distance


class GeneticAlgorithm:
    def __init__(self):
        #초기 10개의 크로모송 모델
        self.chromosomes = [Chromosome() for _ in range(10)]
        #세대
        self.generation = 0
        # 현재 크로모송 인덱스
        self.current_chromosome_index = 0

    def selection(self):
        #앞에서 2개만 사용
        result = self.chromosomes[:2]
        return result

    def crossover(self, chromosome1, chromosome2):
        child1 = Chromosome()
        child2 = Chromosome()

        return child1, child2
    #---------------------------------------------------------------------------------
    # 교차를 이용한 교배 연산
    def single_point_crossover(self, chromosome1, chromosome2):
        pivot = random.randint(1, len(chromosome1) - 1)
        offspring = chromosome1[:pivot] + chromosome2[pivot:]
        offspring = self.static_mutation(offspring, 0.0015)
        return offspring

    # 정적 변이 연산
    def static_mutation(self, chromosome, p):
        result = ''
        for gene in chromosome:
            r = random.random()
            if r <= p:
                print('변이 발생')
                gene = '1' if gene == '0' else '0'
            result += gene
        return result

    #---------------------------------------------------------------------------------
    def mutation(self, chromosome):
        pass

    def next_generation(self):
        next_chromosomes = []
        for i in range(5):
            selected_chromosome = self.selection()

            # ======================== 교배 연산(원코드) =====================
            # child_chromosome1, child_chromosome2 = self.crossover(
            #     selected_chromosome[0],
            #     selected_chromosome[1])
            # =============================================================
            # ======================== 교차 교배 연산 ========================
            child_chromosome1, child_chromosome2 = self.single_point_crossover(
                selected_chromosome[0],
                selected_chromosome[1])
            # =============================================================

            # self.mutation(child_chromosome1)
            # self.mutation(child_chromosome2)

            next_chromosomes.append(child_chromosome1)
            next_chromosomes.append(child_chromosome2)

        self.chromosomes = next_chromosomes
        self.generation += 1
        self.current_chromosome_index = 0