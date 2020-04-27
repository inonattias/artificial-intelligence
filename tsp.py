import random
from tkinter import *
from tkinter import messagebox

import utils
from search import *
from typing import Tuple
from primMST import primMST

distances = {}


# romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)

class TSProblem(Problem):
    """subclass of Problem to define various functions"""

    def __init__(self, graph: Graph):
        super().__init__(initial= tuple(list(graph.graph_dict.keys())[0]))
        assert not graph.directed
        self.graph: Dict[str, Dict[str, float]] = graph.graph_dict
        self.number_of_vertices = graph.number_of_vertices

    def goal_test(self, state: Tuple[str]):
        return len(set(state)) == self.number_of_vertices and \
               len(state) == self.number_of_vertices + 1 and \
               state[0] == state[-1]

    # returns List[actions]
    def actions(self, state: Tuple[str]) -> List[str]:
        if len(state) == self.number_of_vertices:
            return [state[0]]
        return list(filter(lambda x: x not in state, self.graph.get(state[-1]).keys()))

    def __check_action_is_valid(self, state: Tuple[str], action: str) -> bool:
        return action in self.actions(state)

    # returns state
    def result(self, state: Tuple[str], action: str) -> Tuple[str]:
        if not self.__check_action_is_valid(state, action):
            raise RuntimeWarning('action' + action + 'is not valid ')

        ans = state + tuple([action])
        return ans

    def path_cost(self, c, state1: Tuple[str], action, state2: Tuple[str]):
        path_cst = self.graph.get(state1[-1]).get(action)
        if not path_cst or not self.graph.get(state1[-1]).get(state2[-1]):
            raise RuntimeWarning('action' + state1[-1] + ' to ' + state2[-1] + 'is not valid ')
        return c + (path_cst or np.inf)

    def h(self, node: Node) -> float:
        graph = self.graph
        state: Tuple[str] = node.state
        # newGraph: Graph = Graph(dict(filter(lambda e: e[0] in state , graph.items())))
        if not graph:
            raise RuntimeWarning('did not find self.graph in h in TSP')
        if len(state) < 3:
            newGraph = Graph(graph)
        else:
            newGraph = Graph(dict({key: value for (key, value) in graph.items() if key not in state[1:-1]}))

        return primMST(newGraph)




if __name__ == '__main__':
    pass
