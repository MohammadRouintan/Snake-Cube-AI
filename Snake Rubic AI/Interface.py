import numpy as np
import json
from copy import deepcopy
from Environment import *

class Interface:
    def __init__(self):
        pass

    def evolve(self, state:Environment, agent_position, action):
        if type(action) is not str:
            raise "action is not a string"
        action = action.upper()
        if action not in self.valid_actions(state, agent_position):
            raise "action is not valid"
        # if '90' in action:
        #     action = action[0] + '270'
        # elif '270' in action:
        #     action = action[0] + '90'
        #
        # if agent_position < 13 and agent_position != 0:
        #     agent_position -= 1
        # elif agent_position > 13 and agent_position != 26:
        #     agent_position += 1
        # # if agent_position != 13:
        state.take_action(agent_position, action)

    def copy_state(self, state):
        _copy = Environment(None, None)
        _copy.coordinates = deepcopy(state.coordinates)
        _copy.sticky_cubes = state.sticky_cubes
        return _copy

    def perceive(self, state):
        return json.dumps({'coordinates': state.coordinates, 'stick_together': state.sticky_cubes})

    def goal_test(self, state):
        arr = np.array(state.coordinates).astype(int)
        axs = arr.T
        if abs(np.unique(axs[0], return_counts=True)[1] - 9).sum() != 0 or \
                abs(np.unique(axs[1], return_counts=True)[1] - 9).sum() != 0 or \
                abs(np.unique(axs[2], return_counts=True)[1] - 9).sum() != 0:
            return False
        return True

    def valid_actions(self, state: Environment, agent_position):
        valid_acts = ['X90', 'X270', 'X180', 'Y90', 'Y270', 'Y180', 'Z90', 'Z270', 'Z180']

        if agent_position == 0:
            coordinate_0 = state.coordinates[0]
            coordinate_1 = state.coordinates[1]
            print('a')
            if (coordinate_0[2] == coordinate_1[2]):
                return ['Z90', 'Z270', 'Z180']
            if (coordinate_0[1] == coordinate_1[1]):
                return ['Y90', 'Y270', 'Y180']
            if (coordinate_0[0] == coordinate_1[0]):
                return ['X90', 'X270', 'X180']
            
        if agent_position == 26:
            coordinate_26 = state.coordinates[26]
            coordinate_25 = state.coordinates[25]
            if (coordinate_26[2] == coordinate_25[2]):
                return ['Z90', 'Z270', 'Z180']
            if (coordinate_26[1] == coordinate_25[1]):
                return ['Y90', 'Y270', 'Y180']
            if (coordinate_26[0] == coordinate_25[0]):
                return ['X90', 'X270', 'X180']

        pos_i = state.coordinates[agent_position]
        pos_post = state.coordinates[agent_position + 1]
        pos_pre = state.coordinates[agent_position - 1]

        if pos_i[0] == pos_pre[0] and pos_i[0] == pos_post[0] and pos_i[1] == pos_pre[1] and pos_i[1] == pos_post[1]:
            return ['Z90', 'Z270', 'Z180']
        if pos_i[0] == pos_pre[0] and pos_i[0] == pos_post[0] and pos_i[2] == pos_pre[2] and pos_i[2] == pos_post[2]:
            return ['Y90', 'Y270', 'Y180']
        if pos_i[2] == pos_pre[2] and pos_i[2] == pos_post[2] and pos_i[1] == pos_pre[1] and pos_i[1] == pos_post[1]:
            return ['X90', 'X270', 'X180']

        if pos_i[1] == pos_pre[1] and pos_i[1] == pos_post[1]:
            return ['Z90', 'Z270', 'Z180', 'X90', 'X270', 'X180']
        if pos_i[0] == pos_pre[0] and pos_i[0] == pos_post[0]:
            return ['Y90', 'Y270', 'Y180', 'Z90', 'Z270', 'Z180']
        if pos_i[2] == pos_pre[2] and pos_i[2] == pos_post[2]:
            return ['X90', 'X270', 'X180', 'Y90', 'Y270', 'Y180']

        return valid_acts

    def valid_state(self, state):
        axs = state.coordinates
        return len(np.unique(axs, axis=0)) == len(axs)