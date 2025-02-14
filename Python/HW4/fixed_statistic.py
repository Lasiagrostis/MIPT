import random
import numpy

def fixed_statistic(observation, configuration):
    """
    Strategy based on https://avatars.dzeninfra.ru/get-zen_doc/3985649/pub_5faa46b389ace40d9a449e91_5faa816a9c3dc81f90d0e63e/scale_1200
    """
    all_results = [0]*int(configuration.episodeSteps*0.354)+[1]*int(configuration.episodeSteps*0.296) +\
     [2]*int(configuration.episodeSteps*0.35)
    return random.choice(all_results)
