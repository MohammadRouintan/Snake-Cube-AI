import numpy as np
import random
import heapq
import json
import time
from CubeEnvironment import *
from Graphic import Graphic
from Interface import *
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, strategy='A*'):
        self.strategy = strategy
        self.solution_steps = None
        self.axis = {'X': 0, "Y": 1, "Z": 2}
        self.degrees = {"90": 1, '180': 2, "270": 3}
        self.interface = Interface()
        self.gui = Graphic()

    def get_action(self, percept):
        data_sensor = json.loads(percept)
        if self.solution_steps is None:
            initial_state = CubeEnvironment(data_sensor['cube_positions'], data_sensor["stick_together"])
            valid_indices = self.remove_unnecessary_cubes(initial_state)
            if self.strategy == 'BFS':
                self.solution_steps = self.BFS(initial_state, valid_indices)
            elif self.strategy == 'IDS':
                self.solution_steps = self.IDS(initial_state, valid_indices)
            elif self.strategy == 'UCS':
                self.solution_steps = self.UCS(initial_state, valid_indices)
            elif self.strategy == 'A*':
                self.solution_steps = self.A_star(initial_state, valid_indices)
            elif self.strategy == 'RBFS':
                self.solution_steps = self.RBFS(initial_state, valid_indices)
        agent_action = self.solution_steps.pop()

        return agent_action

    def remove_unnecessary_cubes(self, state):
        indexes = list(range(0, 27))
        for cubes in state.sticky_pairs:
            indexes.remove(cubes[1])
        if 0 in indexes:
            indexes.remove(0)
        if 26 in indexes:
            indexes.remove(26)

        return indexes

    def BFS(self, initial_state: CubeEnvironment, valid_indices: list):
        queue = []
        # append the first state as (state, action_history)
        queue.append([initial_state, []])
        while queue:
            # pop first element from queue
            current_state = queue.pop(0)
            random.shuffle(valid_indices)
            for agent_idx in valid_indices:
                actions_list = self.interface.valid_actions(current_state[0], agent_idx)
                random.shuffle(actions_list)
                for action in actions_list:
                    # copy the current state
                    child_state = self.interface.copy_state(current_state[0])
                    self.interface.evolve(child_state, agent_idx, action)
                    # add children to queue
                    queue.append([child_state, [(agent_idx, action)] + current_state[1]])

                    # return if goal test is true
                    if self.interface.goal_test(child_state): return [(agent_idx, action)] + current_state[1]

    def IDS(self, initial_state: CubeEnvironment, valid_indices):
        i = 1
        while True:
            result = self.RDFS([initial_state, []], valid_indices, i)
            if result != 'CUTOFF':
                return result
            i += 1

    def RDFS(self, node: list, valid_indices: list, limit):
        if self.interface.goal_test(node[0]):
            return node[1]
        elif limit == 0:
            return "CUTOFF"

        cutoff_flag = False
        random.shuffle(valid_indices)
        for agent_idx in valid_indices:
            actions_list = self.interface.valid_actions(node[0], agent_idx)
            random.shuffle(actions_list)
            for action in actions_list:
                child_state = self.interface.copy_state(node[0])
                self.interface.evolve(child_state, agent_idx, action)
                result = self.RDFS([child_state, [(agent_idx, action)] + node[1]], valid_indices, limit - 1)
                if result == "CUTOFF":
                    cutoff_flag = True
                elif result != "FAILURE":
                    return result

        if cutoff_flag:
            return "CUTOFF"
        else:
            return "FAILURE"

    def UCS(self, initial_state: CubeEnvironment, valid_indices: list):
        priority_queue = []  # Min-heap
        # Add the initial state to the queue with cost 0
        heapq.heappush(priority_queue, (0, id(initial_state), initial_state, []))  # (cost, unique_id, state, path)

        visited = set()  # To track visited states

        while priority_queue:
            cost, _, current_state, path = heapq.heappop(priority_queue)

            # Serialize the current state's cube_positions for uniqueness
            state_id = json.dumps(current_state.cube_positions)

            if state_id in visited:
                continue
            visited.add(state_id)

            # Check if the goal is reached
            if self.interface.goal_test(current_state):
                return path

            # Generate children
            for agent_idx in valid_indices:
                actions_list = self.interface.valid_actions(current_state, agent_idx)

                for action in actions_list:
                    child_state = self.interface.copy_state(current_state)
                    self.interface.evolve(child_state, agent_idx, action)

                    # Serialize child state
                    child_state_id = json.dumps(child_state.cube_positions)

                    if child_state_id not in visited:
                        # Push the child state with updated cost and path
                        heapq.heappush(priority_queue,
                                       (cost + 1, id(child_state), child_state, [(agent_idx, action)] + path))

    def heuristic(self, state: CubeEnvironment):
        # Example heuristic: Calculate Manhattan distance to align all cubes in a 3x3x3 block
        max_coords = np.max(state.cube_positions, axis=0)
        min_coords = np.min(state.cube_positions, axis=0)

        # The goal is to form a compact 3x3x3 cube
        goal_dimensions = [3, 3, 3]  # Dimensions of the goal cube
        current_dimensions = max_coords - min_coords + 1  # Dimensions of the current cube
        # Sum of differences between current dimensions and goal dimensions
        h = sum(abs(current - goal) for current, goal in zip(current_dimensions, goal_dimensions))
        return h

    def A_star(self, initial_state: CubeEnvironment, valid_indices: list):
        priority_queue = []  # Min-heap
        # Add the initial state to the queue with cost 0 and heuristic h(n)
        heapq.heappush(priority_queue, (0 + self.heuristic(initial_state), 0, id(initial_state), initial_state, []))
        # (f(n), g(n), unique_id, state, path)

        visited = set()  # To track visited states

        while priority_queue:
            f, g, _, current_state, path = heapq.heappop(priority_queue)
            # Serialize the current state's cube_positions for uniqueness
            state_id = json.dumps(current_state.cube_positions)

            if state_id in visited:
                continue
            visited.add(state_id)

            # Check if the goal is reached
            if self.interface.goal_test(current_state):
                return path

            # Generate children
            for agent_idx in valid_indices:
                actions_list = self.interface.valid_actions(current_state, agent_idx)

                for action in actions_list:
                    child_state = self.interface.copy_state(current_state)
                    self.interface.evolve(child_state, agent_idx, action)

                    # Serialize child state
                    child_state_id = json.dumps(child_state.cube_positions)

                    if child_state_id not in visited:
                        g_new = g + 1  # Increment cost
                        f_new = g_new + self.heuristic(child_state)  # Compute f(n) = g(n) + h(n)

                        # Push the child state with updated cost, heuristic, and path
                        heapq.heappush(priority_queue,
                                       (f_new, g_new, id(child_state), child_state, [(agent_idx, action)] + path))
        return None  # Return None if no solution is found


    def RBFS(self, initial_state: CubeEnvironment, valid_indices: list):
        """Recursive Best-First Search algorithm."""
        g = 0  # Cost so far
        h = self.heuristic(initial_state)
        f = g + h
        node = (initial_state, [], f)
        result, _ = self.rbfs_recursive(node, valid_indices, float('inf'))
        return result

    def rbfs_recursive(self, node, valid_indices, f_limit):
        """Helper function for RBFS to handle recursion."""
        state, path, f = node

        if self.interface.goal_test(state):
            return path, f

        successors = []

        # Generate successors
        for agent_idx in valid_indices:
            actions_list = self.interface.valid_actions(state, agent_idx)

            for action in actions_list:
                child_state = self.interface.copy_state(state)
                self.interface.evolve(child_state, agent_idx, action)
                child_path = [(agent_idx, action)] + path

                g = len(child_path)  # Cost so far
                h = self.heuristic(child_state)
                f_child = max(g + h, f)

                child_node = (child_state, child_path, f_child)
                successors.append(child_node)

        if not successors:
            return None, float('inf')  # Failure

        while True:
            # Sort successors based on their f-value
            successors.sort(key=lambda x: x[2])  # x[2] is the f-value

            best = successors[0]
            if best[2] > f_limit:
                return None, best[2]  # Failure

            # Alternative f-cost for the second-best node
            if len(successors) > 1:
                alternative = successors[1][2]
            else:
                alternative = float('inf')

            # Recursive call with the new f_limit
            result, best_f = self.rbfs_recursive(best, valid_indices, min(f_limit, alternative))

            # Update the f-value of the best node after recursion
            successors[0] = (best[0], best[1], best_f)

            if result is not None:
                return result, best_f