import random
import math

my_action = []

def keep_strategy(observation, configuration):
    def get_score(left_move, right_move):
        # This method exists in this file so it can be consumed from rps.py and agents.py without a circular dependency
        delta = (
            right_move - left_move
            if (left_move + right_move) % 2 == 0
            else left_move - right_move
        )
        return 0 if delta == 0 else math.copysign(1, delta)
    global my_action
    if observation.step == 0:
        answer = random.randrange(0, configuration.signs)
        my_action.append(answer)
    elif get_score(my_action[-1], observation.lastOpponentAction) == 1:
        answer = my_action[-1]
        my_action.append(answer)
    else:
        answer = random.randrange(0, configuration.signs)
        my_action.append(answer)
    return answer
