import numpy as np
import json
from copy import deepcopy
from CubeEnvironment import *

class Interface:
    def __init__(self):
        pass

    def evolve(self, state:CubeEnvironment, agent_position, action):
        action = action.upper()
        if action not in self.valid_actions(state, agent_position):
            raise "action is not valid"
        state.perform_action(agent_position, action)

    def copy_state(self, state):
        _copy = CubeEnvironment(None, None)
        _copy.cube_positions = deepcopy(state.cube_positions)
        _copy.sticky_pairs = state.sticky_pairs
        return _copy

    def perceive(self, state):
        return json.dumps({'cube_positions': state.cube_positions, 'stick_together': state.sticky_pairs})

    def goal_test(self, state):
        maxs = np.max(state.cube_positions, axis=0)
        max_x, max_y, max_z = maxs[0], maxs[1], maxs[2]

        for i in range(0, 3):
            for j in range(0, 3):
                for k in range(0, 3):
                    cordinate = [max_x - i, max_y - j, max_z-k]
                    if cordinate not in state.cube_positions:
                        return False
        return True

    def valid_state(self, state):
        axs = state.cube_positions
        return len(np.unique(axs, axis=0)) == len(axs)

    def valid_actions(self, state: CubeEnvironment, agent_position):
        valid_acts = ['X90', 'X270', 'X180', 'Y90', 'Y270', 'Y180', 'Z90', 'Z270', 'Z180']

        if agent_position == 0:
            coordinate_0 = state.cube_positions[0]
            coordinate_1 = state.cube_positions[1]
            if (coordinate_0[2] == coordinate_1[2]):
                return ['Z90', 'Z270', 'Z180']
            if (coordinate_0[1] == coordinate_1[1]):
                return ['Y90', 'Y270', 'Y180']
            if (coordinate_0[0] == coordinate_1[0]):
                return ['X90', 'X270', 'X180']
            
        if agent_position == 26:
            coordinate_26 = state.cube_positions[26]
            coordinate_25 = state.cube_positions[25]
            if (coordinate_26[2] == coordinate_25[2]):
                return ['Z90', 'Z270', 'Z180']
            if (coordinate_26[1] == coordinate_25[1]):
                return ['Y90', 'Y270', 'Y180']
            if (coordinate_26[0] == coordinate_25[0]):
                return ['X90', 'X270', 'X180']

        pos_i = state.cube_positions[agent_position]
        pos_post = state.cube_positions[agent_position + 1]
        pos_pre = state.cube_positions[agent_position - 1]

        if pos_pre[0] == pos_i[0] == pos_post[0] and pos_pre[1] == pos_i[1] == pos_post[1]:
            return ['Z90', 'Z270', 'Z180']
        if pos_pre[0] == pos_i[0] == pos_post[0] and pos_pre[2] == pos_i[2] == pos_post[2]:
            return ['Y90', 'Y270', 'Y180']
        if pos_pre[1] == pos_i[1] == pos_post[1] and pos_pre[2] == pos_i[2] == pos_post[2]:
            return ['X90', 'X270', 'X180']

        if pos_pre[0] == pos_i[0] == pos_post[0]:
            return ['Y90', 'Y270', 'Y180', 'Z90', 'Z270', 'Z180']
        if pos_pre[1] == pos_i[1] == pos_post[1]:
            return ['Z90', 'Z270', 'Z180', 'X90', 'X270', 'X180']
        if pos_pre[2] == pos_i[2] == pos_post[2]:
            return ['X90', 'X270', 'X180', 'Y90', 'Y270', 'Y180']

        return valid_acts