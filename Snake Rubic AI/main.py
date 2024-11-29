import time

from CubeEnvironment import CubeEnvironment
from Graphic import Graphic
from Interface import Interface
from Agent import Agent
import matplotlib.pyplot as plt
import numpy as np


# def plot_rubik(state):
#     tensor = np.zeros(shape=(9, 9, 9))
#     colors = np.zeros(shape=(*tensor.shape, 3))
#     coordinates = np.array(state.cube_positions).astype(int)
#     min = [-coordinates[:, 0].min(), -coordinates[:, 1].min(), -coordinates[:, 2].min()]
#     #  the objects into a single boolean array
#     for i, cube in enumerate(coordinates):
#         tensor[cube[0] + min[0], cube[1] + min[1], cube[2] + min[2]] = 1
#         colors[cube[0] + min[0], cube[1] + min[1], cube[2] + min[2]] = np.array([i / 27, i / 27, i / 27])
#         # combine
# 
#     # and plot everything
#     ax = plt.figure().add_subplot(projection='3d')
# 
#     ax.voxels(tensor, edgecolor='k', facecolors=colors)
# 
#     plt.show()

def run_one_sample(sample_input_json, strategy='BFS'):
    game = CubeEnvironment(sample_input_json['cube_positions'].copy(), sample_input_json['stick_together'].copy())
    interface = Interface()
    agent = Agent(strategy=strategy)
    gui = Graphic()
    # gui.display(game.cube_positions)

    action_count = 0
    st = time.time()
    while not (interface.goal_test(game)):
        action = agent.get_action(interface.perceive(game))
        interface.evolve(game, action[0], action[1])
        # gui.display(game.cube_positions)
        if not interface.valid_state(game): raise 'reached invalid state'
        action_count += 1
    en = time.time()

    return action_count, en - st

sample = {
    "cube_positions": [
        [-5, 2, -6],
        [-5, 2, -5],
        [-5, 2, -4],
        [-4, 2, -4],
        [-3, 2, -4],
        [-3, 2, -3],
        [-3, 2, -2],
        [-2, 2, -2],
        [-1, 2, -2],
        [-1, 2, -1],
        [0, 2, -1],
        [0, 2, 0],
        [0, 1, 0],
        [0, 0, 0],
        [1, 0, 0],
        [2, 0, 0],
        [2, 0, 1],
        [3, 0, 1],
        [3, 0, 2],
        [3, 0, 3],
        [4, 0, 3],
        [4, 0, 4],
        [4, 0, 5],
        [5, 0, 5],
        [5, 0, 6],
        [6, 0, 6],
        [7, 0, 6],
    ],
    "stick_together": [[5, 6], [12, 13], [14, 15], [15, 16], [18, 19]],
}
samples = [
{"cube_positions": [[1, 1, 1], [1, 1, 0], [1, 0, 0], [0, 0, 0], [0, 0, 1], [0, 1, 1], [0, 1, 2], [-1, 1, 2], [-1, 0, 2], [0, 0, 2], [0, -1, 2], [0, -1, 1], [0, -1, 0], [-1, -1, 0], [-2, -1, 0], [-2, -1, 1], [-1, -1, 1], [-1, -1, 2], [-2, -1, 2], [-2, 0, 2], [-2, 0, 1], [-1, 0, 1], [-1, 0, 0], [-2, 0, 0], [-2, 1, 0], [-2, 1, 1], [-2, 1, 2]], "stick_together": [[0, 1], [1, 2], [2, 3], [5, 6], [6, 7], [9, 10], [10, 11], [11, 12], [17, 18], [20, 21], [25, 26]]},
{"cube_positions": [[0, 0, -1], [0, 0, 0], [-1, 0, 0], [-1, 0, -1], [-2, 0, -1], [-2, -1, -1], [-2, -1, 0], [-2, 0, 0], [-2, 0, 1], [-2, -1, 1], [-2, -2, 1], [-1, -2, 1], [-1, -2, 0], [-2, -2, 0], [-2, -2, -1], [-1, -2, -1], [-1, -1, -1], [0, -1, -1], [0, -2, -1], [0, -2, 0], [0, -2, 1], [0, -1, 1], [-1, -1, 1], [-1, -1, 2], [0, -1, 2], [0, 0, 2], [0, 0, 1]], "stick_together": [[1, 2], [4, 5], [9, 10], [11, 12], [13, 14], [15, 16], [17, 18], [18, 19]]},
{"cube_positions": [[2, -1, -2], [1, -1, -2], [1, 0, -2], [2, 0, -2], [2, 0, -1], [2, 0, 0], [2, -1, 0], [2, -1, -1], [1, -1, -1], [0, -1, -1], [0, -1, 0], [1, -1, 0], [1, 0, 0], [1, 0, -1], [0, 0, -1], [0, 0, 0], [0, 1, 0], [-1, 1, 0], [-1, 1, -1], [0, 1, -1], [0, 1, -2], [-1, 1, -2], [-2, 1, -2], [-2, 1, -1], [-2, 1, 0], [-3, 1, 0], [-4, 1, 0]], "stick_together": [[2, 3], [7, 8], [8, 9], [11, 12], [17, 18], [23, 24], [24, 25]]},
{"cube_positions": [[2, 2, -2], [2, 2, -1], [2, 1, -1], [1, 1, -1], [1, 0, -1], [2, 0, -1], [2, 0, 0], [1, 0, 0], [0, 0, 0], [0, 0, 1], [0, 0, 2], [1, 0, 2], [2, 0, 2], [2, -1, 2], [1, -1, 2], [0, -1, 2], [0, -1, 3], [1, -1, 3], [1, -2, 3], [0, -2, 3], [0, -3, 3], [1, -3, 3], [2, -3, 3], [2, -3, 2], [1, -3, 2], [0, -3, 2], [0, -2, 2]], "stick_together": [[1, 2], [5, 6], [8, 9], [10, 11], [12, 13], [17, 18], [20, 21], [21, 22], [24, 25]]},
{"cube_positions": [[0, -2, 0], [0, -1, 0], [0, 0, 0], [0, 0, -1], [0, 0, -2], [0, -1, -2], [0, -1, -1], [0, -2, -1], [0, -2, -2], [-1, -2, -2], [-1, -1, -2], [-1, 0, -2], [-1, 0, -1], [-2, 0, -1], [-2, -1, -1], [-2, -1, 0], [-2, 0, 0], [-1, 0, 0], [-1, -1, 0], [-1, -1, -1], [-1, -2, -1], [-1, -2, 0], [-2, -2, 0], [-2, -2, -1], [-2, -2, -2], [-2, -3, -2], [-2, -4, -2]], "stick_together": [[1, 2], [2, 3], [11, 12], [17, 18], [19, 20], [22, 23]]},
{"cube_positions": [[2, 2, -2], [2, 1, -2], [2, 1, -1], [2, 0, -1], [1, 0, -1], [1, 1, -1], [1, 2, -1], [2, 2, -1], [2, 2, 0], [1, 2, 0], [0, 2, 0], [0, 2, -1], [0, 1, -1], [0, 1, 0], [1, 1, 0], [2, 1, 0], [2, 0, 0], [1, 0, 0], [0, 0, 0], [0, 0, -1], [0, 0, -2], [0, -1, -2], [0, -2, -2], [0, -2, -3], [0, -1, -3], [0, 0, -3], [0, 0, -4]], "stick_together": [[0, 1], [2, 3], [3, 4], [7, 8], [8, 9], [12, 13], [16, 17], [18, 19], [20, 21], [25, 26]]},
{"cube_positions": [[0, 0, -1], [0, 0, -2], [0, -1, -2], [0, -1, -1], [0, -1, 0], [0, 0, 0], [0, 0, 1], [1, 0, 1], [2, 0, 1], [2, -1, 1], [2, -1, 2], [1, -1, 2], [1, 0, 2], [2, 0, 2], [2, 1, 2], [2, 1, 1], [2, 1, 0], [1, 1, 0], [0, 1, 0], [0, 1, 1], [1, 1, 1], [1, 1, 2], [0, 1, 2], [0, 0, 2], [0, -1, 2], [0, -1, 1], [1, -1, 1]], "stick_together": [[1, 2], [6, 7], [7, 8], [9, 10], [11, 12], [13, 14], [14, 15], [15, 16], [17, 18], [21, 22], [24, 25]]},
{"cube_positions": [[2, 2, -2], [3, 2, -2], [3, 2, -1], [3, 2, 0], [4, 2, 0], [4, 2, -1], [4, 1, -1], [3, 1, -1], [3, 0, -1], [2, 0, -1], [2, 1, -1], [2, 2, -1], [2, 2, 0], [1, 2, 0], [0, 2, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0], [0, 0, 0], [0, 0, -1], [0, 0, -2], [0, -1, -2], [0, -2, -2], [-1, -2, -2], [-1, -1, -2], [-1, 0, -2], [-2, 0, -2]], "stick_together": [[1, 2], [6, 7], [10, 11], [18, 19], [23, 24], [25, 26]]},
{"cube_positions": [[-1, -3, 0], [-1, -3, 1], [-1, -3, 2], [0, -3, 2], [0, -2, 2], [1, -2, 2], [1, -2, 1], [1, -2, 0], [1, -1, 0], [1, -1, 1], [1, -1, 2], [0, -1, 2], [-1, -1, 2], [-1, -2, 2], [-1, -2, 1], [-1, -1, 1], [0, -1, 1], [0, -1, 0], [0, 0, 0], [-1, 0, 0], [-1, 1, 0], [-1, 1, -1], [-2, 1, -1], [-2, 1, 0], [-2, 2, 0], [-2, 2, -1], [-2, 2, -2]], "stick_together": [[2, 3], [3, 4], [4, 5], [6, 7], [7, 8], [9, 10], [13, 14], [14, 15], [15, 16], [19, 20], [20, 21], [21, 22], [22, 23]]},
{"cube_positions": [[1, 2, 0], [2, 2, 0], [2, 1, 0], [2, 1, 1], [2, 0, 1], [1, 0, 1], [0, 0, 1], [0, 0, 0], [0, -1, 0], [0, -1, -1], [0, 0, -1], [-1, 0, -1], [-2, 0, -1], [-2, -1, -1], [-1, -1, -1], [-1, -1, -2], [-1, 0, -2], [-2, 0, -2], [-2, 0, -3], [-1, 0, -3], [0, 0, -3], [0, -1, -3], [0, -2, -3], [0, -2, -2], [-1, -2, -2], [-1, -2, -3], [-2, -2, -3]], "stick_together": [[1, 2], [2, 3], [8, 9], [9, 10], [12, 13], [14, 15], [15, 16], [17, 18], [18, 19]]},
{"cube_positions": [[0, 1, 2], [-1, 1, 2], [-2, 1, 2], [-2, 1, 1], [-2, 1, 0], [-2, 0, 0], [-2, 0, 1], [-1, 0, 1], [-1, 0, 2], [-2, 0, 2], [-2, -1, 2], [-1, -1, 2], [-1, -1, 1], [-2, -1, 1], [-2, -1, 0], [-1, -1, 0], [0, -1, 0], [0, -1, 1], [0, -1, 2], [0, 0, 2], [0, 0, 1], [0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0], [1, 0, 1], [1, 1, 1]], "stick_together": [[1, 2], [8, 9], [9, 10], [14, 15], [20, 21]]},
{"cube_positions": [[-1, 1, -1], [0, 1, -1], [0, 0, -1], [0, 0, 0], [0, -1, 0], [-1, -1, 0], [-1, -1, -1], [0, -1, -1], [1, -1, -1], [1, -1, 0], [1, -1, 1], [2, -1, 1], [3, -1, 1], [3, -2, 1], [2, -2, 1], [1, -2, 1], [1, -3, 1], [2, -3, 1], [2, -3, 0], [1, -3, 0], [1, -3, -1], [2, -3, -1], [3, -3, -1], [3, -2, -1], [2, -2, -1], [1, -2, -1], [1, -2, 0]], "stick_together": [[0, 1], [1, 2], [5, 6], [7, 8], [10, 11], [13, 14], [14, 15], [16, 17], [17, 18], [18, 19], [19, 20], [21, 22], [23, 24], [24, 25], [25, 26]]},
]

if __name__ == "__main__":
    for sm in samples:
        for strategy in ['BFS', 'IDS', 'UCS', 'A*']:
            cost = run_one_sample(sm, strategy=strategy)
            print(f'Strategy = {strategy}, Action Count = {cost[0]}, Time = {cost[1]}')
        print()