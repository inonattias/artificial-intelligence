import math
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
        super().__init__(initial=tuple(list(graph.graph_dict.keys())[0]))
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
        raise NotImplementedError

    def h_name(self) -> str:
        raise NotImplementedError


class TSProblemMST(TSProblem):
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

    def h_name(self) -> str:
        return 'Minimum spanning tree'


class TSProblemSP(TSProblem):

    def h(self, node: Node) -> float:
        init = '1'
        graph: Dict[str, Dict[str, float]] = self.graph
        state: Tuple[str] = node.state
        if init == state[-1]:
            return 0.0
        return graph[state[-1]][init]

    def h_name(self) -> str:
        return 'Shortest path'


def _calc_shortest_edges(graph: Graph, state: Tuple[str], n: int):
    g: Dict[str, Dict[str, float]] = graph.graph_dict
    legal_edge: List[float] = []
    v_forbidden: List[str] = list(state[1:-1])
    for v1, edges in g.items():
        v_forbidden.append(v1)
        for v2, length in edges.items():
            if v2 in v_forbidden:
                break
            else:
                legal_edge.append(g[v1][v2])

    legal_edge.sort()
    return sum(legal_edge[:n])


class TSProblemShortestEdges(TSProblem):

    def h(self, node: Node) -> float:
        init = '1'
        graph: Dict[str, Dict[str, float]] = self.graph
        state: Tuple[str] = node.state
        if len(state) < 3:
            newGraph = Graph(graph)
        else:
            newGraph = Graph(dict({key: value for (key, value) in graph.items() if key not in state[1:-1]}))
        return _calc_shortest_edges(newGraph, state, self.number_of_vertices - len(state) + 1)

    def h_name(self) -> str:
        return 'Shortest Edges'


class TSProblemLongestWayAndBack(TSProblem):
    def _find_longest_road_and_back(self, v: str, state: Tuple[str]):
        init = '1'
        edges = self.graph[v]
        long_road_value = 0
        ans_v: str = None
        for v2, value in edges.items():
            if v2 not in state and value > long_road_value:
                long_road_value = value
                ans_v = v2
        if ans_v:
            return long_road_value + self.graph[ans_v]['1']
        else:
            if v == '1':
                return 0.0
            return self.graph[v]['1']

    def h(self, node: Node) -> float:

        state: Tuple[str] = node.state

        return self._find_longest_road_and_back(state[-1], state)

    def h_name(self) -> str:
        return 'Long path'


class TSProblemMSTp2(TSProblem):

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

        return primMST(newGraph) + _calc_shortest_edges(newGraph, state, 2)
        # g = newGraph.graph_dict
        # all_edges: List[float] = []
        #
        # for v1, edges in g.items():
        #     for v2, length in edges.items():
        #             all_edges.append(g[v1][v2])
        # all_edges.sort(reverse=True)
        #
        # return primMST(newGraph) + sum(all_edges[-1:])

    def h_name(self) -> str:
        return 'Minimum spanning tree + two shortest paths'


if __name__ == '__main__':
    pass
