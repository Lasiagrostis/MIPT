import random
def statistical(observation, configuration):
  ## Объявляем глобальную переменную для хранения гистограммы действий
    global action_histogram
    if observation.step == 0:
      # На первом шаге инициализируем гистограмму действий
        action_histogram = {}
        return
    action = observation.lastOpponentAction # Получаем последнее действие противника

    #Если действие противника отсутствует в гистограмме, добавляем его
    if action not in action_histogram:
        action_histogram[action] = 0
    action_histogram[action] += 1
    mode_action = None    #Переменная для хранения наиболее частого действия
    mode_action_count = None  # Переменная для хранения частоты этого действия


# Итерируем по всем записям гистограммы для поиска наиболее частого действия
    for k, v in action_histogram.items():
        if mode_action_count is None or v > mode_action_count:
            mode_action = k
            mode_action_count = v
            continue

    return (mode_action + 1) % configuration.signs
