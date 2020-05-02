import time

from typing import List, Tuple, Dict

from tspAnnealingProblem import TSPAnnealingProblem, calc_sum_of_path, calc_ham_sum_of_path
from gui import Gui
from simulated_annealing import get_best_alpha_params, get_best_beta_params
from utils import distance
import os
import errno
from search import Graph, astar_search, Node
from primMST import primMST
from tsp import TSProblem, TSProblemMST, TSProblemSP, TSProblemShortestEdges, TSProblemLongestWayAndBack, TSProblemMSTp2

number_of_files_to_run = 1
input_prefix = 'Input/'
input_files_paths: List[str] = ['tsp131_xy.txt']
input_files_paths = [input_prefix + s for s in input_files_paths]

output_prefix = 'Output/'
output_files_paths: List[str] = ['tsp131_s.txt']
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


def draw_graph_from_result(cord: List[Tuple[float, float]], result_state: List[str], algo_name: str = ""):
    path = [cord[int(label) - 1] for label in result_state[:-1]]
    Gui(path, result_state[:-1], algo_name).draw_graph()


def a_start_with_time(tsp_problem: TSProblem, index: int) -> Node:
    start = time.time()
    res = a_star_for_tsp(tsp_problem, index)
    end = time.time()
    print("Time took:" + str(end - start))
    return res


def a_star_for_tsp(tsp_problem: TSProblem, index: int) -> Node:
    result_node: Node = astar_search(tsp_problem, display=True)
    print('tsp sum:' + str(result_node.path_cost))
    print('hamilton sum' + str(result_node.parent.path_cost))
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
            # res =a_star_for_tsp(TSProblemMSTp2(g), index)
            # a_star_for_tsp(TSProblemLongestWayAndBack(g), index)
            # a_star_for_tsp(TSProblemSP(g), index)
            # a_star_for_tsp(TSProblemShortestEdges(g), index)
            # a_star_for_tsp(TSProblemMST(g), index)
            # draw_graph_from_result(cord, list(a_start_with_time(TSProblemMST(g), index).state))
            # draw_graph_from_result(cord, a_start_with_time(TSProblemMSTp2(g), index).state)

            # path, value = simulated_annealing1(TSPAnnealingProblem(g))
            # path.append(path[0])
            # draw_graph_from_result(cord, path, "simulated Annealing")

            # print(path)
            # get_best_alpha_params(TSPAnnealingProblem(g), [1e9],
            #                      [0.995, 0.996], 30)
            ans = get_best_alpha_params(TSPAnnealingProblem(g), [1e9], [0.9995], 30)
            # print(len(ans))
            # 760 / 755.5
            # ans2 = ['1', '5', '13', '18', '25', '17', '19', '26', '28', '29', '30', '55', '54', '64', '68', '75', '62', '65', '69', '82', '93', '98', '112', '114', '121', '118', '123', '130', '131', '129', '116', '120', '122', '117', '111', '103', '104', '97', '96', '95', '90', '91', '73', '61', '41', '40', '42', '24', '44', '43', '59', '60', '72', '80', '83', '88', '92', '94', '99', '102', '107', '108', '109', '110', '115', '119', '128', '127', '126', '125', '124', '113', '106', '100', '105', '101', '87', '84','86', '85', '81', '78', '77', '89', '74', '53', '45', '46', '27', '16', '12', '15', '14', '20', '31', '32', '21', '33', '50', '51', '52', '47', '48', '49', '34', '35', '22', '37', '36', '58', '57', '66', '79', '71', '76', '70', '63', '67', '56', '39', '38', '23', '11', '4', '10', '9', '3', '2', '8', '7', '6']

            # print(calc_ham_sum_of_path(ans2,g.graph_dict))
            # 939
            # ans =['19', '29', '47', '49', '51', '52', '57', '67', '63', '58', '39', '40', '23', '11', '24', '42', '60', '97', '104', '103', '111', '94', '92', '81', '82', '87', '99', '113', '124', '121', '123', '130', '131', '119', '115', '109', '88', '69', '62', '36', '37', '38', '59', '73', '72', '76', '71', '66', '70', '65', '78', '75', '64', '68', '77', '93', '107', '106', '118', '114', '105', '102', '101', '100', '112', '98', '89', '74', '45', '53', '18', '13', '5', '1', '7', '21', '22', '8', '2', '3', '4', '10', '9', '6', '12', '14', '15', '20', '32', '34', '33', '48', '55', '54', '46', '31', '35', '41', '43', '44', '61', '91', '90', '95', '96', '110', '116', '120', '117', '122', '129', '128', '127', '126', '125', '108', '86', '85', '84', '83', '80', '79', '56', '50', '30', '28', '27', '26', '25', '17', '16']
            write_results_to_file(output_files_paths[index], ans)
            draw_graph_from_result(cord, ans, "Simulated Annealing")


if __name__ == '__main__':
    main()
