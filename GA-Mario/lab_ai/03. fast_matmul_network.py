# 03. fast_matmul_network.py

import numpy as np
#class는 금형이라고 생각하고 매번 변수를 생성하는 것이 아닌 틀을 찍어냄으로 써 형태를 항상 유지한 상태에서 찍어낸 것에 변수를 가미?함
# w1, b1 : 선을 표현하는 애 input-hidden 사이
# w2, b2 : 선을 표현하는 애 hidden-output 사이

class Model:
    def __init__(self):
        self.relu = lambda x: np.maximum(0, x)
        self.sigmoid = lambda x: 1.0 / (1.0 + np.exp(-x))

        # (x w1) -> (l1 w2) -> y
        self.w1 = np.random.uniform(low=-1, high=1, size=(13 * 16, 9))
        self.b1 = np.random.uniform(low=-1, high=1, size=(9,))

        self.w2 = np.random.uniform(low=-1, high=1, size=(9, 6))
        self.b2 = np.random.uniform(low=-1, high=1, size=(6,))

    def predict(self, data):
        l1 = np.matmul(data, self.w1) + self.b1
        l1_output = self.relu(l1)

        l2 = np.matmul(l1_output, self.w2) + self.b2
        l2_output = self.sigmoid(l2)

        predict = l2_output
        print(predict)

        result = (predict > 0.5).astype(np.int)
        print(result)

        return result



if __name__ == '__main__':
    n = 3
    # generation = [Model() for _ in range(n)]
    # generation = []
    # for _ in range(n):
    #     generation.append(Model())

    model = Model()
    data = np.random.randint(0, 3, (13 * 16,), dtype=np.int)
    print(model.predict(data))