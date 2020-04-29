from random import random, shuffle, sample

from search import Problem, Node, Graph
from simulated_annealing import exp_schedule
import numpy as np
from typing import Tuple, Dict, List
from tsp import distances
from utils import probability


def _calc_sum_of_path(lst: List[str], g: Graph) -> float:
    graph_dict = g.graph_dict
    sum: float = 0.0
    for index, node in enumerate(lst):
        if index == len(lst):
            sum += graph_dict[node][lst[0]]
        else:
            sum += graph_dict[node][lst[index + 1]]
    return sum


def _calc_random_order(lst: List[str]) -> List[str]:
    return shuffle(lst)


def _calc_initial(graph: Graph) -> Tuple[List[str], float]:
    initial_list: List[str] = list(graph.graph_dict.keys())
    initial_list = _calc_random_order(initial_list)
    return initial_list, _calc_sum_of_path(initial_list, graph)


class TSPAnnealingProblem:

    def __init__(self, graph: Graph):
        self.initial = _calc_initial(graph)
        assert not graph.directed
        self.graph: Dict[str, Dict[str, float]] = graph.graph_dict
        self.n = graph.number_of_vertices
        # returns List[actions]

    def _calc_new_state_sum(self, current_path: List[str], items_to_swap: List[str], old_sum: float) -> float:
        assert len(items_to_swap) == 2
        k, m = current_path.index(items_to_swap[0]), current_path.index(items_to_swap[1])
        prev_k = k - 1 if k != 0 else self.n
        prev_m = m - 1 if m != 0 else self.n
        next_k = k + 1 if k != self.n else 0
        next_m = m + 1 if m != self.n else 0
        return old_sum + self.graph[current_path[prev_k]][current_path[m]] + \
               self.graph[current_path[m]][current_path[next_k]] + \
               self.graph[current_path[prev_m]][current_path[k]] + \
               self.graph[current_path[k]][current_path[next_m]] - \
               self.graph[current_path[prev_m]][current_path[m]] - \
               self.graph[current_path[m]][current_path[next_m]] - \
               self.graph[current_path[prev_k]][current_path[k]] - \
               self.graph[current_path[k]][current_path[next_k]]

    def get_random_next_state(self, current_state: Tuple[List[str], float]) -> Tuple[List[str], float]:
        path, cur_sum = current_state
        items_to_swap: List[2] = list(sample(path, 2))
        a, b = path.index(items_to_swap[0]), path.index(items_to_swap[1])
        path[b], path[a] = path[a], path[b]
        return path, self._calc_new_state_sum(current_state[0], path, cur_sum)
