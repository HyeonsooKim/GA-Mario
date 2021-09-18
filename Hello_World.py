import re as r

# print('Hyeonsoo Kim')
#
# print('I can do this all day')
#
# print("Can you feel my heartbeat?")

import numpy as np
import random

a = np.array([i for i in range(10)])
print(a)
random.shuffle(a)
print(a)

b = a[a>=5]
print(a>=5)
print(b)

def simulated_binary_crossover(parent_chromosome1, parent_chromosome2):
    #eta의 역할 : 커질수록 미세하게 조정 됨
    rand = np.random.random(parent_chromosome1.shape)
    gamma = np.empty(parent_chromosome1.shape)
    gamma[rand <= 0.5] = (2 * rand[rand<=0.5] ** (1.0 / (100+1)))
    gamma[rand > 0.5] = (2 * rand[rand > 0.5] ** (1.0 / (100+1)))
    child_chromosome1 = 0.5 * ((1 + gamma) * parent_chromosome1 + (1 - gamma) * parent_chromosome2)
    child_chromosome2 = 0.5 * ((1 - gamma) * parent_chromosome1 + (1 + gamma) * parent_chromosome2)
    return child_chromosome1, child_chromosome2

