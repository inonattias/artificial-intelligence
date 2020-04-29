from random import shuffle, sample

from search import Graph

from typing import Tuple, Dict, List


def _calc_sum_of_path(lst: List[str], graph_dict: Dict[str, Dict[str, float]]) -> float:
    sum: float = 0.0
    for index, node in enumerate(lst):
        if index == len(lst) - 1:
            sum += graph_dict[node][lst[0]]
        else:
            sum += graph_dict[node][lst[index + 1]]
    return sum


def _calc_random_order(lst: List[str]) -> List[str]:
    shuffle(lst)
    return lst


def _calc_initial(graph: Graph) -> Tuple[List[str], float]:
    initial_list: List[str] = list(graph.graph_dict.keys())
    initial_list = _calc_random_order(initial_list)
    return initial_list, _calc_sum_of_path(initial_list, graph.graph_dict)


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

        prev_k = k - 1 if k != 0 else self.n - 1
        prev_m = m - 1 if m != 0 else self.n - 1
        next_k = k + 1 if k != self.n - 1 else 0
        next_m = m + 1 if m != self.n - 1 else 0

        if prev_k == m:
            return old_sum + self.graph[current_path[prev_m]][current_path[k]] + \
                   self.graph[current_path[m]][current_path[next_k]] - \
                   self.graph[current_path[prev_m]][current_path[m]] - \
                   self.graph[current_path[k]][current_path[next_k]]
        elif next_k == m:
            return old_sum + self.graph[current_path[prev_k]][current_path[m]] + \
                   self.graph[current_path[k]][current_path[next_m]] - \
                   self.graph[current_path[m]][current_path[next_m]] - \
                   self.graph[current_path[prev_k]][current_path[k]]

        return old_sum + self.graph[current_path[prev_k]][current_path[m]] + \
               self.graph[current_path[m]][current_path[next_k]] + \
               self.graph[current_path[prev_m]][current_path[k]] + \
               self.graph[current_path[k]][current_path[next_m]] - \
               self.graph[current_path[prev_m]][current_path[m]] - \
               self.graph[current_path[m]][current_path[next_m]] - \
               self.graph[current_path[prev_k]][current_path[k]] - \
               self.graph[current_path[k]][current_path[next_k]]

    def get_random_next_state(self, current_state: Tuple[List[str], float]) -> Tuple[List[str], float]:
        cur_path, cur_sum = current_state
        new_path =cur_path.copy()
        items_to_swap: List[2] = list(sample(cur_path, 2))
        a, b = new_path.index(items_to_swap[0]), new_path.index(items_to_swap[1])
        new_path[b], new_path[a] = new_path[a], new_path[b]
        my_sum = self._calc_new_state_sum(cur_path, items_to_swap, cur_sum)
        assert int(my_sum) == int(_calc_sum_of_path(new_path,self.graph)), "calc_sum:"+str(my_sum) +"True sum:"+str(_calc_sum_of_path(new_path,self.graph))
        return new_path, my_sum
