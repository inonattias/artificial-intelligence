import random
from tkinter import *
from tkinter import messagebox

import utils
from search import *
from typing import Tuple

distances = {}


# romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)

class TSProblem(Problem):
    """subclass of Problem to define various functions"""

    def __init__(self, graph: Graph):
        super().__init__(initial=([]))
        assert not graph.directed
        self.graph: Dict[str, Dict[str, float]] = graph.graph_dict
        self.number_of_vertices = graph.number_of_vertices

    def goal_test(self, state: List[str]):
        return len(set(state)) == self.number_of_vertices and \
               len(state) == len(set(state)) and \
               state[0] == state[self.number_of_vertices - 1]

    def actions(self, state: List[str]) -> List[str]:
        return list(filter(lambda x: x not in state, self.graph.get(state[-1]).keys()))

    def __check_action_is_valid(self, path_so_far: List[str], action: str) -> bool:
        return action in self.actions(path_so_far)

    def result(self, state: List[str], action: str) -> List[str]:
        if not self.__check_action_is_valid(state, action):
            raise RuntimeWarning('action' + action + 'is not valid ')
        return state.append(action)

    def path_cost(self, cost_so_far, A: str, B: str):
        if not self.graph.get(A, B):
            raise RuntimeWarning('action' + A + ' to ' + B + 'is not valid ')
        return cost_so_far + (self.graph.get(A, B) or np.inf)

    def value(self, path_so_far: List[str]) -> float:
        """value of path cost given negative for the given state"""
        return self.path_cost(path_so_far)

    def min_span_tree_heuristic(self, node: Node):
        locs = getattr(self.graph, 'locations', None)
        if locs:
            if type(node) is str:
                return int(distance(locs[node], locs[self.goal]))

            return int(distance(locs[node.state], locs[self.goal]))
        else:
            return np.inf


if __name__ == '__main__':
    pass
