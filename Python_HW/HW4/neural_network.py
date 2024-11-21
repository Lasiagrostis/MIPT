import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Инициализация модели нейронной сети
model = Sequential([
    Dense(32, input_shape=(6,), activation="relu"),  # Входные данные — 6 последних ходов
    Dense(32, activation="relu"),
    Dense(3, activation="softmax")  # Выход — вероятности для "Камень", "Бумага", "Ножницы"
])

# Компиляция модели
model.compile(optimizer="adam", loss="categorical_crossentropy")

# Инициализация памяти ходов с начальным значением
history = [0, 0, 0, 0, 0, 0]  # Начальная последовательность, чтобы избежать ошибок при первых шагах

def neural_network_agent(observation, configuration):
    global history

    # Добавляем предыдущий ход соперника и наш ход в историю
    if observation.step > 0:
        history.extend([observation.lastOpponentAction, history[-1]])

    # Если данных недостаточно, выбираем случайный ход
    if len(history) < 6:
        action = int(np.random.randint(3))
        history.append(action)
        return action

    # Формируем входные данные из последних 6 ходов
    input_data = np.array(history[-6:]).reshape(1, -1)

    # Прогнозируем следующий ход соперника
    opponent_pred = np.argmax(model.predict(input_data)[0])

    # Выбираем действие, которое побеждает предсказанный ход соперника
    action = (opponent_pred + 1) % 3
    history.append(action)

    # Отключаем обучение в реальном времени для стабильности (опционально включить для обучения)
    # target = np.zeros(3)
    # target[observation.lastOpponentAction] = 1
    # model.fit(input_data, target.reshape(1, -1), epochs=1, verbose=0)

    return int(action)
