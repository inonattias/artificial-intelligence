from typing import Dict, List, Set, Tuple
from search import Graph


def primMST(graph: Graph) -> float:
    graph_dict: Dict[str, Dict[str, float]] = graph.graph_dict
    V: List[str] = list(graph_dict.keys())
    T: Set[Tuple[str, str]] = set()
    X: Set[str] = set()
    sum_of_MST: float = 0.0

    X.add(V[0])

    while len(X) != graph.number_of_vertices:
        crossing: Set[Tuple[str, str]] = set()
        for x in X:
            for k in V:
                if k not in X and graph_dict.get(x).get(k) > 0.0:
                    crossing.add((x, k))
        edge = sorted(crossing, key=lambda e: graph_dict.get(e[0]).get(e[1]))[0]
        T.add(edge)
        X.add(edge[1])
        sum_of_MST += graph_dict.get(edge[0]).get(edge[1])

    for edge in T:
        print(str(edge))

    return sum_of_MST


if __name__ == '__main__':
    romania_map = Graph(dict(
        Arad=dict(Bucharest=75.0, Craiova=140.0),
        Bucharest=dict(Arad=75.0, Craiova=101.0),
        Craiova=dict(Arad=140.0, Bucharest=101.0)), False)
    print(primMST(romania_map))
