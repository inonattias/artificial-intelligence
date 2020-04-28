from typing import List, Tuple, Dict

from gui import draw_graph
from utils import distance
import os
import errno
from search import Graph, astar_search, Node
from primMST import primMST
from tsp import TSProblem

number_of_files_to_run = 1
input_prefix = 'Input/'
input_files_paths: List[str] = ['tsp15_xy.txt', 'tsp48_xy.txt', 'tsp131_xy.txt']
input_files_paths = [input_prefix + s for s in input_files_paths]

output_prefix = 'Output/'
output_files_paths: List[str] = ['tsp15_s.txt', 'tsp48_s.txt', 'tsp131_s.txt']
output_files_paths = [output_prefix + s for s in output_files_paths]


def create_graph_from_points(cord_list: List[Tuple[float, float]]) -> Graph:
    graph_dict: Dict[str, Dict[str, float]] = {}
    for index, cord in enumerate(cord_list):
        tmp_cord_dict = dict()
        for sec_index, sec_cord in enumerate(cord_list):
            if index != sec_index:
                tmp_cord_dict[str(sec_index + 1)] = distance(cord, sec_cord)
        graph_dict[str(index + 1)] = tmp_cord_dict
    return Graph(graph_dict, False)


def write_results_to_file(output_file_path: str, path: Tuple[str]):
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    if not os.path.exists(os.path.dirname(output_file_path)):
        try:
            os.makedirs(os.path.dirname(output_file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(output_file_path, 'w+') as f:
        for node in path[:-1]:
            f.write(node + '\n')


def main():
    for index, input_file_file_path in enumerate(input_files_paths[:number_of_files_to_run]):
        with open(input_file_file_path, 'r') as input_file:
            cord: List[Tuple[float, float]] = []
            for line in input_file.readlines():
                (x, y) = line.split()
                cord.append((float(x), float(y)))
            g = create_graph_from_points(cord)
            print(g)

            tsp = TSProblem(g)
            result_node: Node = astar_search(tsp, display=True)
            print(result_node.state)
            print(result_node.path())
            write_results_to_file(output_files_paths[index], result_node.state)

            path = [cord[int(label)-1] for label in result_node.state[:-1]]
            draw_graph(path, result_node.state[:-1])


if __name__ == '__main__':
    main()
