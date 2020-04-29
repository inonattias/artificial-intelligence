import time

from typing import List, Tuple, Dict

from tspAnnealingProblem import TSPAnnealingProblem
from gui import draw_graph
from simulated_annealing import simulated_annealing1
from utils import distance
import os
import errno
from search import Graph, astar_search, Node
from primMST import primMST
from tsp import TSProblem, TSProblemMST, TSProblemSP, TSProblemShortestEdges, TSProblemLongestWayAndBack, TSProblemMSTp2

number_of_files_to_run = 1
input_prefix = 'Input/'
input_files_paths: List[str] = ['tsp131_xy.txt', 'tsp131_xy.txt']
input_files_paths = [input_prefix + s for s in input_files_paths]

output_prefix = 'Output/'
output_files_paths: List[str] = [ 'tsp131_xy.txt', 'tsp131_s.txt']
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


def draw_graph_from_result(cord: List[Tuple[float, float]], result_node: Node):
    path = [cord[int(label) - 1] for label in result_node.state[:-1]]
    draw_graph(path, result_node.state[:-1])


def a_start_with_time(tsp_problem: TSProblem, index: int) -> Node:
    start = time.time()
    res = a_star_for_tsp(tsp_problem, index)
    end = time.time()
    print("Time took:" + str(end - start))
    return res


def a_star_for_tsp(tsp_problem: TSProblem, index: int) -> Node:
    result_node: Node = astar_search(tsp_problem, display=True)
    print('Result for' + tsp_problem.h_name() + str(result_node.state))
    print(result_node.path())
    write_results_to_file(output_files_paths[index], result_node.state)
    return result_node


def main():
    for index, input_file_file_path in enumerate(input_files_paths[:number_of_files_to_run]):
        with open(input_file_file_path, 'r') as input_file:
            cord: List[Tuple[float, float]] = []
            for line in input_file.readlines():
                if not line.split():
                    continue
                (x, y) = line.split()
                cord.append((float(x), float(y)))
            g = create_graph_from_points(cord)
            print(g)
            #res =a_star_for_tsp(TSProblemMSTp2(g), index)
            #a_star_for_tsp(TSProblemLongestWayAndBack(g), index)
            # a_star_for_tsp(TSProblemSP(g), index)
            # a_star_for_tsp(TSProblemShortestEdges(g), index)
             ##a_star_for_tsp(TSProblemMST(g), index)
            # draw_graph_from_result(cord, a_start_with_time(TSProblemMST(g), index))
            # draw_graph_from_result(cord, a_start_with_time(TSProblemMSTp2(g), index))
            path,value = simulated_annealing1(TSPAnnealingProblem(g))
            print(path)


if __name__ == '__main__':
    main()
