from typing import List, Tuple, Dict
from utils import distance

from search import Graph, astar_search
from primMST import primMST
from tsp import TSProblem

number_of_files_to_run = 1
prefix = 'Input/'
input_files_paths: List[str] = ['tsp15_xy.txt', 'tsp48_xy.txt', 'tsp131_xy.txt']
input_files_paths = [prefix + s for s in input_files_paths]


def create_graph_from_points(cord_list: List[Tuple[float, float]]) -> Graph:
    graph_dict: Dict[str, Dict[str, float]] = {}
    for index, cord in enumerate(cord_list):
        tmp_cord_dict = dict()
        for sec_index, sec_cord in enumerate(cord_list):
            if index != sec_index:
                tmp_cord_dict[str(sec_index)] = distance(cord, sec_cord)
        graph_dict[str(index)] = tmp_cord_dict
    return Graph(graph_dict, False)


def main():
    for file_path in input_files_paths[:number_of_files_to_run]:
        with open(file_path, 'r') as input_file:
            cord: List[Tuple[float, float]] = []
            for line in input_file.readlines():
                (x, y) = line.split()
                cord.append((float(x), float(y)))
            print(create_graph_from_points(cord))

            tsp = TSProblem(create_graph_from_points(cord))
            astar_search(tsp, primMST)


if __name__ == '__main__':
    main()
