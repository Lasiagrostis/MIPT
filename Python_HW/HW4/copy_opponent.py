
import random  # Добавляем импорт random

def copy_opponent(observation, configuration):
    # Если у нас есть информация о последнем ходе противника
    if observation.step > 0:
        return observation.lastOpponentAction
    # Начальный шаг
    else:
        return random.randrange(0, configuration.signs)
