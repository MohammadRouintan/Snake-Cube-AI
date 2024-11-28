import numpy as np
import json
from copy import deepcopy

class Environment:
    def __init__(self, coordinates, sticky_cubes):
        self.coordinates = coordinates
        self.sticky_cubes = sticky_cubes

    def is_sticky_cube(self, agent_position):
        return [agent_position, agent_position + 1] in self.sticky_cubes

    def is_linear_cube(self, agent_position):
        if agent_position == 0 or agent_position == 26:
            return True

        pos_i = self.coordinates[agent_position]
        pos_post = self.coordinates[agent_position + 1]
        pos_pre = self.coordinates[agent_position - 1]

        if pos_i[0] == pos_pre[0] and pos_i[0] == pos_post[0] and pos_i[1] == pos_pre[1] and pos_i[1] == pos_post[1]:
            return True
        if pos_i[0] == pos_pre[0] and pos_i[0] == pos_post[0] and pos_i[2] == pos_pre[2] and pos_i[2] == pos_post[2]:
            return True
        if pos_i[1] == pos_pre[1] and pos_i[1] == pos_post[1] and pos_i[2] == pos_pre[2] and pos_i[2] == pos_post[2]:
            return True

        return False

    def execute_action(self, agent_position, cube_position, action):

        agent_coordinate = self.coordinates[agent_position]
        cube_coordinate = self.coordinates[cube_position]
        new_coordinate = self.change_coordinate(agent_coordinate, cube_coordinate, action)

        return new_coordinate

    def change_coordinate(self, agent_coordinate, cube_coordinate, action):
        new_coordinate = None
        if '90' in action:
            axis = action[0]
            if axis == "X":
                new_coordinate = [cube_coordinate[0], 0, 0]
                new_coordinate[1] = agent_coordinate[2] - \
                    cube_coordinate[2] + agent_coordinate[1]
                new_coordinate[2] = cube_coordinate[1] - \
                    agent_coordinate[1] + agent_coordinate[2]
            if axis == "Y":
                new_coordinate = [0, cube_coordinate[1], 0]
                new_coordinate[0] = -agent_coordinate[2] + \
                    cube_coordinate[2] + agent_coordinate[0]
                new_coordinate[2] = -cube_coordinate[0] + \
                    agent_coordinate[0] + agent_coordinate[2]
            if axis == "Z":
                new_coordinate = [0, 0, cube_coordinate[2]]
                new_coordinate[1] = cube_coordinate[0] - \
                    agent_coordinate[0] + agent_coordinate[1]
                new_coordinate[0] = agent_coordinate[1] - \
                    cube_coordinate[1] + agent_coordinate[0]

        if '180' in action:
            axis = action[0]
            if axis == "X":
                new_coordinate = [cube_coordinate[0], 0, 0]
                new_coordinate[1] = 2 * \
                    agent_coordinate[1] - cube_coordinate[1]
                new_coordinate[2] = 2 * \
                    agent_coordinate[2] - cube_coordinate[2]
            if axis == "Y":
                new_coordinate = [0, cube_coordinate[1], 0]
                new_coordinate[0] = 2 * \
                    agent_coordinate[0] - cube_coordinate[0]
                new_coordinate[2] = 2 * \
                    agent_coordinate[2] - cube_coordinate[2]
            if axis == "Z":
                new_coordinate = [0, 0, cube_coordinate[2]]
                new_coordinate[1] = 2 * \
                    agent_coordinate[1] - cube_coordinate[1]
                new_coordinate[0] = 2 * \
                    agent_coordinate[0] - cube_coordinate[0]

        if '270' in action:
            axis = action[0]
            if axis == "X":
                new_coordinate = [cube_coordinate[0], 0, 0]
                new_coordinate[1] = cube_coordinate[2] - \
                                    agent_coordinate[2] + agent_coordinate[1]
                new_coordinate[2] = agent_coordinate[1] - \
                                    cube_coordinate[1] + agent_coordinate[2]
            if axis == "Y":
                new_coordinate = [0, cube_coordinate[1], 0]
                new_coordinate[0] = -cube_coordinate[2] + \
                                    agent_coordinate[2] + agent_coordinate[0]
                new_coordinate[2] = -agent_coordinate[0] + \
                                    cube_coordinate[0] + agent_coordinate[2]
            if axis == "Z":
                new_coordinate = [0, 0, cube_coordinate[2]]
                new_coordinate[1] = agent_coordinate[0] - \
                                    cube_coordinate[0] + agent_coordinate[1]
                new_coordinate[0] = cube_coordinate[1] - \
                                    agent_coordinate[1] + agent_coordinate[0]

        return new_coordinate

    def take_action(self, agent_position, action):
        temp_coordinate = deepcopy(self.coordinates)

        if not self.is_sticky_cube(agent_position) and self.is_linear_cube(agent_position):
            return

        if self.is_sticky_cube(agent_position):
            idx = agent_position
            if self.is_linear_cube(idx):
                sub_coordinates = self.coordinates[0: idx+1]

                for i in range(idx+1, 27):
                    new_coordinate = self.execute_action(idx, i, action)
                    if new_coordinate not in sub_coordinates:
                        self.coordinates[i] = new_coordinate
                    else:
                        self.coordinates = temp_coordinate
                        return

        if not self.is_linear_cube(agent_position):
            if 'X' in action:
                if self.coordinates[agent_position + 1][0] == self.coordinates[agent_position][0]:
                    sub_coordinates = self.coordinates[:agent_position + 1]
                    for i in range(agent_position + 1, 27):

                        new_coordinate = self.execute_action(agent_position, i, action)
                        if new_coordinate not in sub_coordinates:
                            self.coordinates[i] = new_coordinate
                        else:
                            self.coordinates = temp_coordinate
                            return

                else:
                    sub_coordinates = self.coordinates[agent_position:]
                    for i in range(0, agent_position):
                        new_coordinate = self.execute_action(agent_position, i, action)
                        if new_coordinate not in sub_coordinates:
                            self.coordinates[i] = new_coordinate
                        else:
                            self.coordinates = temp_coordinate
                            return

            elif 'Y' in action:
                if self.coordinates[agent_position + 1][1] == self.coordinates[agent_position][1]:
                    sub_coordinates = self.coordinates[:agent_position + 1]
                    for i in range(agent_position + 1, 27):

                        new_coordinate = self.execute_action(agent_position, i, action)

                        if new_coordinate not in sub_coordinates:
                            self.coordinates[i] = new_coordinate
                        else:
                            self.coordinates = temp_coordinate
                            return
                else:
                    sub_coordinates = self.coordinates[agent_position:]
                    for i in range(0, agent_position):

                        new_coordinate = self.execute_action(agent_position, i, action)

                        if new_coordinate not in sub_coordinates:
                            self.coordinates[i] = new_coordinate
                        else:
                            self.coordinates = temp_coordinate
                            return

            elif 'Z' in action:
                if self.coordinates[agent_position + 1][2] == self.coordinates[agent_position][2]:
                    sub_coordinates = self.coordinates[:agent_position+1]
                    for i in range(agent_position + 1, 27):

                        new_coordinate = self.execute_action(
                            agent_position, i, action)

                        if new_coordinate not in sub_coordinates:
                            self.coordinates[i] = new_coordinate
                        else:
                            self.coordinates = temp_coordinate
                            return
                else:
                    sub_coordinates = self.coordinates[agent_position:]
                    for i in range(0, agent_position):

                        new_coordinate = self.execute_action(agent_position, i, action)

                        if new_coordinate not in sub_coordinates:
                            self.coordinates[i] = new_coordinate
                        else:
                            self.coordinates = temp_coordinate
                            return