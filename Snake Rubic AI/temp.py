import numpy as np
import json
from copy import deepcopy

class CubeEnvironment:
    def __init__(self, cube_positions, sticky_pairs):
        self.cube_positions = cube_positions
        self.sticky_pairs = sticky_pairs

    def is_sticky_pair(self, current_index):
        return [current_index, current_index + 1] in self.sticky_pairs

    def is_aligned_cube(self, current_index):
        if current_index == 0 or current_index == 26:
            return True

        current_pos = self.cube_positions[current_index]
        next_pos = self.cube_positions[current_index + 1]
        prev_pos = self.cube_positions[current_index - 1]

        if (current_pos[0] == prev_pos[0] == next_pos[0] and
            current_pos[1] == prev_pos[1] == next_pos[1]):
            return True
        if (current_pos[0] == prev_pos[0] == next_pos[0] and
            current_pos[2] == prev_pos[2] == next_pos[2]):
            return True
        if (current_pos[1] == prev_pos[1] == next_pos[1] and
            current_pos[2] == prev_pos[2] == next_pos[2]):
            return True

        return False

    def apply_rotation(self, cube_index, target_index, rotation):
        current_cube = self.cube_positions[cube_index]
        target_cube = self.cube_positions[target_index]
        updated_position = self.rotate_cube(current_cube, target_cube, rotation)

        return updated_position

    def rotate_cube(self, current, target, rotation):
        updated = None
        if '90' in rotation:
            axis = rotation[0]
            if axis == "X":
                updated = [target[0], 0, 0]
                updated[1] = current[2] - target[2] + current[1]
                updated[2] = target[1] - current[1] + current[2]
            elif axis == "Y":
                updated = [0, target[1], 0]
                updated[0] = -current[2] + target[2] + current[0]
                updated[2] = -target[0] + current[0] + current[2]
            elif axis == "Z":
                updated = [0, 0, target[2]]
                updated[1] = target[0] - current[0] + current[1]
                updated[0] = current[1] - target[1] + current[0]

        elif '180' in rotation:
            axis = rotation[0]
            if axis == "X":
                updated = [target[0], 0, 0]
                updated[1] = 2 * current[1] - target[1]
                updated[2] = 2 * current[2] - target[2]
            elif axis == "Y":
                updated = [0, target[1], 0]
                updated[0] = 2 * current[0] - target[0]
                updated[2] = 2 * current[2] - target[2]
            elif axis == "Z":
                updated = [0, 0, target[2]]
                updated[1] = 2 * current[1] - target[1]
                updated[0] = 2 * current[0] - target[0]

        elif '270' in rotation:
            axis = rotation[0]
            if axis == "X":
                updated = [target[0], 0, 0]
                updated[1] = target[2] - current[2] + current[1]
                updated[2] = current[1] - target[1] + current[2]
            elif axis == "Y":
                updated = [0, target[1], 0]
                updated[0] = -target[2] + current[2] + current[0]
                updated[2] = -current[0] + target[0] + current[2]
            elif axis == "Z":
                updated = [0, 0, target[2]]
                updated[1] = current[0] - target[0] + current[1]
                updated[0] = target[1] - current[1] + current[0]

        return updated

    def perform_action(self, current_index, rotation):
        original_positions = deepcopy(self.cube_positions)

        if not self.is_sticky_pair(current_index) and self.is_aligned_cube(current_index):
            return

        if self.is_sticky_pair(current_index):
            idx = current_index
            if self.is_aligned_cube(idx):
                preserved_positions = self.cube_positions[:idx+1]

                for i in range(idx+1, 27):
                    updated_position = self.apply_rotation(idx, i, rotation)
                    if updated_position not in preserved_positions:
                        self.cube_positions[i] = updated_position
                    else:
                        self.cube_positions = original_positions
                        return

        if not self.is_aligned_cube(current_index):
            if 'X' in rotation:
                if self.cube_positions[current_index + 1][0] == self.cube_positions[current_index][0]:
                    preserved_positions = self.cube_positions[:current_index + 1]
                    for i in range(current_index + 1, 27):
                        updated_position = self.apply_rotation(current_index, i, rotation)
                        if updated_position not in preserved_positions:
                            self.cube_positions[i] = updated_position
                        else:
                            self.cube_positions = original_positions
                            return
                else:
                    preserved_positions = self.cube_positions[current_index:]
                    for i in range(0, current_index):
                        updated_position = self.apply_rotation(current_index, i, rotation)
                        if updated_position not in preserved_positions:
                            self.cube_positions[i] = updated_position
                        else:
                            self.cube_positions = original_positions
                            return

            elif 'Y' in rotation:
                if self.cube_positions[current_index + 1][1] == self.cube_positions[current_index][1]:
                    preserved_positions = self.cube_positions[:current_index + 1]
                    for i in range(current_index + 1, 27):
                        updated_position = self.apply_rotation(current_index, i, rotation)
                        if updated_position not in preserved_positions:
                            self.cube_positions[i] = updated_position
                        else:
                            self.cube_positions = original_positions
                            return
                else:
                    preserved_positions = self.cube_positions[current_index:]
                    for i in range(0, current_index):
                        updated_position = self.apply_rotation(current_index, i, rotation)
                        if updated_position not in preserved_positions:
                            self.cube_positions[i] = updated_position
                        else:
                            self.cube_positions = original_positions
                            return

            elif 'Z' in rotation:
                if self.cube_positions[current_index + 1][2] == self.cube_positions[current_index][2]:
                    preserved_positions = self.cube_positions[:current_index+1]
                    for i in range(current_index + 1, 27):
                        updated_position = self.apply_rotation(current_index, i, rotation)
                        if updated_position not in preserved_positions:
                            self.cube_positions[i] = updated_position
                        else:
                            self.cube_positions = original_positions
                            return
                else:
                    preserved_positions = self.cube_positions[current_index:]
                    for i in range(0, current_index):
                        updated_position = self.apply_rotation(current_index, i, rotation)
                        if updated_position not in preserved_positions:
                            self.cube_positions[i] = updated_position
                        else:
                            self.cube_positions = original_positions
                            return
