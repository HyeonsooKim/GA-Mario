# 02. keras_neural_network.py
import tensorflow as tf
import numpy as np

# 순차적은 흐름을 만들어내는 모델을 만듦
model = tf.keras.Sequential([
    tf.keras.layers.Dense(9, input_shape=(13*16), activation='relu'),   #9개로 설정하는 건 그냥 임의로 한 것
    tf.keras.layers.Dense(6, activation='sigmoid')
])

print(model.summary())

data = np.random.randint(0, 3, (13 * 16,), dtype=np.int)
print(data)

predict = model.predict(np.array([data]))[0]
print(predict)

result = (predict > 0.5).astype(np.int)
print(result)