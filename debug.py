#!env python

from qlearn import QLearn
import config as cfg
import pickle
import os
from pprint import pprint

###########################################
# Debug Q Values from QLearningMouse
#
# Curtis Long 20190221
###########################################

f = open("resources/world.txt",'r')
lines = f.readlines()
f.close()

height = len(lines)
width = max([len(x) for x in lines])

ai = QLearn(actions=range(cfg.directions), alpha=cfg.alpha, gamma=cfg.gamma, epsilon=cfg.epsilon)
if (os.path.isfile('mouse.pickle')):
    with open('mouse.pickle', 'rb') as p:
        ai.q = pickle.load(p)

pprint(ai.q)
print('Items: ' + str(len(ai.q)))
#exit()

dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
actions = range(cfg.directions)
i = 0
j = 0
for line in lines:
    print("\n", end='')
    line = line.rstrip('\n')
    for i in range(len(line)):
        if (line[i] == 'X'):
            print(line[i], end='')
        else:
            #state = tuple([lambda x: 1 if lines[j+x[0]][i+x[1]] == 'X' else 0 for dir in dirs])
            def get_value(x):
                return 1 if lines[j+x[0]][i+x[1]] == 'X' else 0

            state = map(get_value, dirs)
            #pprint(str(state))
            state = tuple(state)
            #action = ai.choose_action(state)
            q = [ai.q.get((state, act),0) for act in actions]
            max_utility = max(q)
            # In case there're several state-action max values
            # we select a random one among them
            if q.count(max_utility) > 1:
                ch = 'r'
            else:
                action = actions[q.index(max_utility)]
                # serious code issue from QLearningMouse here - directions are translated differently TODO debug
                # dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                # dx, dy = [(0, -1), (1, -1), ( 1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
                if (action == 0):
                    ch ='↖' # up left
                elif (action == 1):
                    ch ='←' # left
                elif (action == 2):
                    ch ='↙' # down left
                elif (action == 3):
                    ch ='↑' # up
                elif (action == 4):
                    ch ='↓' # down
                elif (action == 5):
                    ch ='↗' # up right
                elif (action == 6):
                    ch ='→' # right
                elif (action == 7):
                    ch ='↘' # down right
            print(ch, end='')
    j = j + 1

