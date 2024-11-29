import numpy as np
import json
from copy import deepcopy

class CubeEnvironment:
    def __init__(self, cube_positions, sticky_cubes):
        self.cube_positions = cube_positions
        self.sticky_pairs = sticky_cubes

    def is_sticky_pair(self, agent_position):
        return [agent_position, agent_position + 1] in self.sticky_pairs

    def is_aligned_cube(self, agent_position):
        if agent_position == 0 or agent_position == 26:
            return True

        pos_i = self.cube_positions[agent_position]
        pos_post = self.cube_positions[agent_position + 1]
        pos_pre = self.cube_positions[agent_position - 1]

        if pos_pre[0] == pos_i[0] == pos_post[0] and pos_pre[1] == pos_i[1] == pos_post[1]:
            return True
        if pos_pre[0] == pos_i[0] == pos_post[0] and pos_pre[2] == pos_i[2] == pos_post[2]:
            return True
        if pos_pre[1] == pos_i[1] == pos_post[1] and pos_pre[2] == pos_i[2] == pos_post[2]:
            return True

        return False

    def apply_rotation(self, agent_position, cube_position, action):
        agent_coordinate = self.cube_positions[agent_position]
        cube_coordinate = self.cube_positions[cube_position]
        updated = self.rotate_cube(agent_coordinate, cube_coordinate, action)

        return updated

    def rotate_cube(self, agent_coordinate, cube_coordinate, action):
        updated = None
        if '90' in action:
            axis = action[0]
            if axis == "X":
                updated = [cube_coordinate[0], 0, 0]
                updated[1] = agent_coordinate[2] - \
                    cube_coordinate[2] + agent_coordinate[1]
                updated[2] = cube_coordinate[1] - \
                    agent_coordinate[1] + agent_coordinate[2]
            if axis == "Y":
                updated = [0, cube_coordinate[1], 0]
                updated[0] = -agent_coordinate[2] + \
                    cube_coordinate[2] + agent_coordinate[0]
                updated[2] = -cube_coordinate[0] + \
                    agent_coordinate[0] + agent_coordinate[2]
            if axis == "Z":
                updated = [0, 0, cube_coordinate[2]]
                updated[1] = cube_coordinate[0] - \
                    agent_coordinate[0] + agent_coordinate[1]
                updated[0] = agent_coordinate[1] - \
                    cube_coordinate[1] + agent_coordinate[0]

        if '180' in action:
            axis = action[0]
            if axis == "X":
                updated = [cube_coordinate[0], 0, 0]
                updated[1] = 2 * \
                    agent_coordinate[1] - cube_coordinate[1]
                updated[2] = 2 * \
                    agent_coordinate[2] - cube_coordinate[2]
            if axis == "Y":
                updated = [0, cube_coordinate[1], 0]
                updated[0] = 2 * \
                    agent_coordinate[0] - cube_coordinate[0]
                updated[2] = 2 * \
                    agent_coordinate[2] - cube_coordinate[2]
            if axis == "Z":
                updated = [0, 0, cube_coordinate[2]]
                updated[1] = 2 * \
                    agent_coordinate[1] - cube_coordinate[1]
                updated[0] = 2 * \
                    agent_coordinate[0] - cube_coordinate[0]

        if '270' in action:
            axis = action[0]
            if axis == "X":
                updated = [cube_coordinate[0], 0, 0]
                updated[1] = cube_coordinate[2] - \
                                    agent_coordinate[2] + agent_coordinate[1]
                updated[2] = agent_coordinate[1] - \
                                    cube_coordinate[1] + agent_coordinate[2]
            if axis == "Y":
                updated = [0, cube_coordinate[1], 0]
                updated[0] = -cube_coordinate[2] + \
                                    agent_coordinate[2] + agent_coordinate[0]
                updated[2] = -agent_coordinate[0] + \
                                    cube_coordinate[0] + agent_coordinate[2]
            if axis == "Z":
                updated = [0, 0, cube_coordinate[2]]
                updated[1] = agent_coordinate[0] - \
                                    cube_coordinate[0] + agent_coordinate[1]
                updated[0] = cube_coordinate[1] - \
                                    agent_coordinate[1] + agent_coordinate[0]

        return updated

    def perform_action(self, agent_position, action):
        temp_coordinate = deepcopy(self.cube_positions)
        if not self.is_sticky_pair(agent_position) and self.is_aligned_cube(agent_position):
            return

        if self.is_sticky_pair(agent_position):
            idx = agent_position
            if self.is_aligned_cube(idx):
                sub_coordinates = self.cube_positions[0: idx + 1]

                for i in range(idx+1, 27):
                    updated = self.apply_rotation(idx, i, action)
                    if updated not in sub_coordinates:
                        self.cube_positions[i] = updated
                    else:
                        self.cube_positions = temp_coordinate
                        return

        if not self.is_aligned_cube(agent_position):
            if 'X' in action:
                if self.cube_positions[agent_position + 1][0] == self.cube_positions[agent_position][0]:
                    sub_coordinates = self.cube_positions[:agent_position + 1]
                    for i in range(agent_position + 1, 27):

                        updated = self.apply_rotation(agent_position, i, action)
                        if updated not in sub_coordinates:
                            self.cube_positions[i] = updated
                        else:
                            self.cube_positions = temp_coordinate
                            return

                else:
                    sub_coordinates = self.cube_positions[agent_position:]
                    for i in range(0, agent_position):
                        updated = self.apply_rotation(agent_position, i, action)
                        if updated not in sub_coordinates:
                            self.cube_positions[i] = updated
                        else:
                            self.cube_positions = temp_coordinate
                            return

            elif 'Y' in action:
                if self.cube_positions[agent_position + 1][1] == self.cube_positions[agent_position][1]:
                    sub_coordinates = self.cube_positions[:agent_position + 1]
                    for i in range(agent_position + 1, 27):

                        updated = self.apply_rotation(agent_position, i, action)

                        if updated not in sub_coordinates:
                            self.cube_positions[i] = updated
                        else:
                            self.cube_positions = temp_coordinate
                            return
                else:
                    sub_coordinates = self.cube_positions[agent_position:]
                    for i in range(0, agent_position):

                        updated = self.apply_rotation(agent_position, i, action)

                        if updated not in sub_coordinates:
                            self.cube_positions[i] = updated
                        else:
                            self.cube_positions = temp_coordinate
                            return

            elif 'Z' in action:
                if self.cube_positions[agent_position + 1][2] == self.cube_positions[agent_position][2]:
                    sub_coordinates = self.cube_positions[:agent_position + 1]
                    for i in range(agent_position + 1, 27):

                        updated = self.apply_rotation(agent_position, i, action)

                        if updated not in sub_coordinates:
                            self.cube_positions[i] = updated
                        else:
                            self.cube_positions = temp_coordinate
                            return
                else:
                    sub_coordinates = self.cube_positions[agent_position:]
                    for i in range(0, agent_position):

                        updated = self.apply_rotation(agent_position, i, action)

                        if updated not in sub_coordinates:
                            self.cube_positions[i] = updated
                        else:
                            self.cube_positions = temp_coordinate
                            return