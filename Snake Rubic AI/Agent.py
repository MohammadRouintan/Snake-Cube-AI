import numpy as np
import random
import heapq
import json
import time
from Environment import *
from Graphic import Graphic
from Interface import *
import matplotlib.pyplot as plt


def plot_rubik(state):
    tensor = np.zeros(shape=(9, 9, 9))
    colors = np.zeros(shape=(*tensor.shape, 3))
    coordinates = np.array(state.coordinates).astype(int)
    min = [-coordinates[:, 0].min(), -coordinates[:, 1].min(), -coordinates[:, 2].min()]
    #  the objects into a single boolean array
    for i, cube in enumerate(coordinates):
        tensor[cube[0] + min[0], cube[1] + min[1], cube[2] + min[2]] = 1
        colors[cube[0] + min[0], cube[1] + min[1], cube[2] + min[2]] = np.array([i / 27, i / 27, i / 27])
        # combine

    # and plot everything
    ax = plt.figure().add_subplot(projection='3d')

    ax.voxels(tensor, edgecolor='k', facecolors=colors)

    plt.show()

class Agent:
    def __init__(self, type='IDS'):
        self.type = type
        self.solutions = None
        self.axis = {'X': 0, "Y": 1, "Z": 2}
        self.degrees = {"90": 1, '180': 2, "270": 3}
        self.interface = Interface()
        self.gui = Graphic()

    def get_action(self, percept):
        data_sensor = json.loads(percept)
        if self.solutions is None:
            initial_state = Environment(data_sensor['coordinates'], data_sensor["stick_together"])
            valid_indices = self.remove_unnecessary_cubes(initial_state)
            # if 13 in valid_indices:
            #     valid_indices.remove(13)
            if self.type == 'BFS':
                self.solutions = self.BFS(initial_state, valid_indices)
            elif self.type == 'IDS':
                self.solutions = self.IDS(initial_state, valid_indices)
            elif self.type == 'UCS':
                self.solutions = self.UCS(initial_state, valid_indices)
            elif self.type == 'A*':
                self.solutions = self.A_star(initial_state, valid_indices)
            elif self.type == 'RBFS':
                self.solutions = self.RBFS(initial_state, valid_indices)
        print('sol', self.solutions)
        agent_action = self.solutions.pop()
        # action = [agent_action[0], self.axis[agent_action[1][0]], self.degrees[agent_action[1][1:]]]

        return agent_action

    def remove_unnecessary_cubes(self, state):
        indexes = list(range(0, 27))
        for cubes in state.sticky_cubes:
            indexes.remove(cubes[1])
        if 0 in indexes:
            indexes.remove(0)
        if 26 in indexes:
            indexes.remove(26)

        return indexes

    def BFS(self, initial_state: Environment, valid_indices: list):
        interface = Interface()
        queue = []
        # append the first state as (state, action_history)
        queue.append([initial_state, []])
        while queue:
            # pop first element from queue
            game_state = queue.pop(0)
            random.shuffle(valid_indices)

            for agent_idx in valid_indices:

                actions_list = interface.valid_actions(game_state[0], agent_idx)
                random.shuffle(actions_list)

                for action in actions_list:
                    # copy the current state
                    child_state = interface.copy_state(game_state[0])
                    interface.evolve(child_state, agent_idx, action)
                    # add children to queue
                    queue.append([child_state, [(agent_idx, action)] + game_state[1]])

                    # return if goal test is true
                    if interface.goal_test(child_state): return [(agent_idx, action)] + game_state[1]

    def IDS(self, initial_state: Environment, valid_indices):
        i = 1
        while True:
            print(i)
            result = self.RDFS([initial_state, []], valid_indices, i, [])
            print(result)
            if result != 'CUTOFF':
                return result
            i += 1

    def RDFS(self, node: list, valid_indices: list, limit, prev):
        if self.interface.goal_test(node[0]):
            return node[1]
        elif limit == 0:
            # h = self.heuristic(node[0])
            # if node[0].coordinates[13] != [0, 0, 0]:
            # print(node[0].coordinates[13])
                # if self.heuristic(node[0]) == 2:
                #     print(node[1])
            # self.gui.display(node[0].coordinates)
            return "CUTOFF"

        cutoff_flag = False
        # random.shuffle(valid_indices)
        for agent_idx in valid_indices:
            if agent_idx not in prev:
                actions_list = self.interface.valid_actions(node[0], agent_idx)
                # random.shuffle(actions_list)
                # if self.heuristic(node[0]) == 2:
                #     # print(actions_list)
                #     actions_list = []
                for action in actions_list:
                    child_state = self.interface.copy_state(node[0])
                    self.interface.evolve(child_state, agent_idx, action)
                    if len(set(tuple(coord) for coord in child_state.coordinates)) != 27:
                        continue
                    result = self.RDFS([child_state, [(agent_idx, action)] + node[1]], valid_indices, limit - 1, prev)
                    if result == "CUTOFF":
                        cutoff_flag = True
                    elif result != "FAILURE":
                        return result

        if cutoff_flag:
            return "CUTOFF"
        else:
            return "FAILURE"

    def UCS(self, initial_state: Environment, valid_indices: list):
        interface = Interface()
        priority_queue = []  # Min-heap
        # Add the initial state to the queue with cost 0
        heapq.heappush(priority_queue, (0, id(initial_state), initial_state, []))  # (cost, unique_id, state, path)

        visited = set()  # To track visited states

        while priority_queue:
            cost, _, current_state, path = heapq.heappop(priority_queue)

            # Serialize the current state's coordinates for uniqueness
            state_id = json.dumps(current_state.coordinates)

            if state_id in visited:
                continue
            visited.add(state_id)

            # Check if the goal is reached
            if interface.goal_test(current_state):
                return path

            # Generate children
            for agent_idx in valid_indices:
                actions_list = interface.valid_actions(current_state, agent_idx)

                for action in actions_list:
                    child_state = interface.copy_state(current_state)
                    interface.evolve(child_state, agent_idx, action)

                    # Serialize child state
                    child_state_id = json.dumps(child_state.coordinates)

                    if child_state_id not in visited:
                        # Push the child state with updated cost and path
                        heapq.heappush(priority_queue,
                                       (cost + 1, id(child_state), child_state, [(agent_idx, action)] + path))

    def heuristic(self, state: Environment):
        # Example heuristic: Calculate Manhattan distance to align all cubes in a 3x3x3 block
        # max_coords = np.max(state.coordinates, axis=0)
        # min_coords = np.min(state.coordinates, axis=0)
        #
        # # The goal is to form a compact 3x3x3 cube
        # goal_dimensions = [3, 3, 3]  # Dimensions of the goal cube
        # current_dimensions = max_coords - min_coords + 1  # Dimensions of the current cube
        #
        # mul_goal = 1
        # mul_curr = 1
        # for c, g in zip(current_dimensions, goal_dimensions):
        #     mul_curr *= c
        #     mul_goal *= g
        #
        # h = mul_curr - mul_goal
        # return h
        # Example heuristic: Calculate Manhattan distance to align all cubes in a 3x3x3 block
        max_coords = np.max(state.coordinates, axis=0)
        min_coords = np.min(state.coordinates, axis=0)

        # The goal is to form a compact 3x3x3 cube
        goal_dimensions = [3, 3, 3]  # Dimensions of the goal cube
        current_dimensions = max_coords - min_coords + 1  # Dimensions of the current cube
        # Sum of differences between current dimensions and goal dimensions
        h = sum(abs(current - goal) for current, goal in zip(current_dimensions, goal_dimensions))
        return h

    def A_star(self, initial_state: Environment, valid_indices: list):
        interface = Interface()
        priority_queue = []  # Min-heap
        # Add the initial state to the queue with cost 0 and heuristic h(n)
        heapq.heappush(priority_queue, (0 + self.heuristic(initial_state), 0, id(initial_state), initial_state, []))
        # (f(n), g(n), unique_id, state, path)

        visited = set()  # To track visited states

        while priority_queue:
            f, g, _, current_state, path = heapq.heappop(priority_queue)
            # print(f, g)
            # Serialize the current state's coordinates for uniqueness
            state_id = json.dumps(current_state.coordinates)
            # print('h', self.heuristic(current_state))
            # self.gui.display(current_state.coordinates)

            if state_id in visited:
                continue
            visited.add(state_id)

            # Check if the goal is reached
            if interface.goal_test(current_state):
                return path

            # Generate children
            for agent_idx in valid_indices:
                actions_list = interface.valid_actions(current_state, agent_idx)

                for action in actions_list:
                    child_state = interface.copy_state(current_state)
                    interface.evolve(child_state, agent_idx, action)

                    # Serialize child state
                    child_state_id = json.dumps(child_state.coordinates)

                    if child_state_id not in visited:
                        g_new = g + 1  # Increment cost
                        f_new = g_new + self.heuristic(child_state)  # Compute f(n) = g(n) + h(n)

                        # Push the child state with updated cost, heuristic, and path
                        heapq.heappush(priority_queue,
                                       (f_new, g_new, id(child_state), child_state, [(agent_idx, action)] + path))
        return None  # Return None if no solution is found

    def RBFS(self, initial_state: Environment, valid_indices: list):
        """
        Recursive Best-First Search (RBFS) algorithm.
        """
        interface = Interface()

        # Start the recursive RBFS process
        _, solution = self.RBFS_recursive(
            initial_state,
            valid_indices,
            float('inf'),
            0,  # Initial cost (g(n))
            []
        )

        return solution

    def RBFS_recursive(self, current_state: Environment, valid_indices: list, f_limit, g, path):
        """
        Recursive helper function for RBFS.
        :param current_state: Current state of the search.
        :param valid_indices: List of valid indices for actions.
        :param f_limit: Current best alternative path cost.
        :param g: Path cost so far.
        :param path: Path of actions taken to reach the current state.
        :return: (new f_limit, solution path or None if failure).
        """
        interface = Interface()

        # Check if the goal is reached
        if interface.goal_test(current_state):
            return None, path

        # Generate successors
        successors = []
        for agent_idx in valid_indices:
            actions_list = interface.valid_actions(current_state, agent_idx)
            for action in actions_list:
                child_state = interface.copy_state(current_state)
                interface.evolve(child_state, agent_idx, action)

                # Compute g and f values for the child state
                g_new = g + 1
                f_new = max(g_new + self.heuristic(child_state), g_new)

                # Add to successors
                successors.append((f_new, g_new, agent_idx, action, child_state))

        # If there are no successors, return failure
        if not successors:
            return float('inf'), None

        # Sort successors by their f-values
        successors.sort(key=lambda x: x[0])
        while True:
            # Get the best successor
            best = successors[0]
            best_f = best[0]

            # If the best f-value exceeds f_limit, return failure
            if best_f > f_limit:
                return best_f, None

            # Get the second-best f-value
            alternative = successors[1][0] if len(successors) > 1 else float('inf')

            # Recursive call to explore the best path
            new_f_limit = min(f_limit, alternative)
            result_f, solution = self.RBFS_recursive(
                best[4],  # child_state
                valid_indices,
                new_f_limit,
                best[1],  # g value of the best successor
                [(best[2], best[3])] + path  # Update path
            )

            # Update the f-value of the best successor
            # successors[0] = (result_f, best[1], best[2], best[3], best[4])
            #
            # # Sort successors by their updated f-values
            # successors.sort(key=lambda x: x[0])

            # If a solution is found, return it
            if solution is not None:
                return result_f, solution

