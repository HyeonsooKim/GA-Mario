# 02. keras_neural_network.py
import tensorflow as tf
import numpy as np

# 순차적인 흐름을 만들어내는 모델을 만듦
model = tf.keras.Sequential([
    tf.keras.layers.Dense(9, input_shape=(13 * 16,), activation='relu'), #Hidden 9 개, input은 13*16개
    tf.keras.layers.Dense(6, activation='sigmoid')                       #output 갯수는 6개 - 6개의 캐릭터로 조작
])
#모든 input과 hidden은 모두 연결되어있어야하고, 모든 hidden과 output은 모두 연결되어있어야함
# input - hidden 사이의 선 : 13*16  * 9
# input 행렬에 간선행렬을 곱하면 hidden 행렬
# hidden - output 사이의 선 : 9  *  6
# hidden 행렬에 간선행렬을 곱하면 output 행렬
print(model.summary())


data = np.random.randint(0, 3, (13 * 16,), dtype=np.int)
print(data)

predict = model.predict(np.array([data]))[0]
print(predict)

result = (predict > 0.5).astype(np.int)
print(result)

for bb in range(0,3):
    print('a')

# 입력값/출력값의 동그라미 갯수는 정해져 있고 중간의 Hidden영역의 동그라미 갯수만 조정이 가능함
