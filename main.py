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
            ans = get_best_beta_params(TSPAnnealingProblem(g), [1e9], [5000], 1)

            #ans_48_final_707 = ['1', '8', '9', '38', '31', '44', '18', '7', '6', '37', '19', '27', '17', '43', '30', '28', '36', '33', '46', '15', '40', '3', '23', '11', '12', '20', '47', '13', '21', '32', '39', '48', '5', '42', '10', '24', '45', '35', '4', '26', '2','29', '25', '14', '34', '41', '16', '22']
            #ans = ['55', '46', '45', '53', '74', '89', '93', '98', '112', '124', '125', '126', '127', '131', '130', '123', '121', '118', '114', '105', '100', '101', '102', '106', '113', '110', '111', '103', '104', '117', '122', '129', '128', '120', '116', '119', '115', '109', '108', '107', '99', '94', '92', '88', '87', '81', '78', '77', '75', '68', '64', '54', '26', '27', '28', '29', '30', '31', '33', '32', '20', '19', '25', '17', '15', '14', '16', '18', '13', '5', '12', '6', '1', '7', '22', '36', '37', '38', '23', '39', '40', '41', '42', '43', '44', '58', '63', '67', '84', '85', '86', '90', '91', '97', '96', '95', '82', '66', '57', '35', '34', '21', '8', '2', '3', '9', '10', '4', '11', '24', '61', '60', '59', '73', '72', '80', '83', '79', '76', '71', '70', '69', '65', '62', '56', '52', '51', '50', '49', '48', '47']

            #ans = ['1', '7', '22', '36', '37', '38', '23', '39', '40', '41', '42', '43', '44', '58', '63', '67', '84', '85', '86', '90', '91', '97', '96', '95', '82', '66', '57', '35', '34', '21', '8', '2', '3', '9', '10', '4', '11', '24', '61', '60', '59', '73', '72', '80', '83', '79', '76', '71', '70', '69', '65', '62', '56', '52', '51', '50', '49', '48', '47','55', '46', '45', '53', '74', '89', '93', '98', '112', '124', '125', '126', '127', '131', '130', '123', '121', '118', '114', '105', '100', '101', '102', '106', '113', '110', '111', '103', '104', '117', '122', '129', '128', '120', '116', '119', '115', '109', '108', '107', '99', '94', '92', '88', '87', '81', '78', '77', '75', '68', '64', '54', '26', '27', '28', '29', '30', '31', '33', '32', '20', '19', '25', '17', '15', '14', '16', '18', '13', '5', '12', '6']

            # ans_131 =['24', '11', '4', '10', '23', '39', '38', '37', '36', '50', '78', '77', '75', '64', '68', '46', '54', '55', '47', '48', '49', '34', '33', '21', '31', '30', '29', '28', '27', '26', '53', '45', '74', '89', '100', '105', '121', '118', '114', '124', '125', '126', '127', '129', '122', '117', '116', '120', '111', '103', '104', '97', '96', '95', '90', '91', '73', '72', '58', '57', '56', '52', '35', '22', '9', '3', '2', '8', '7', '1', '12', '15', '14', '6', '5', '13', '18', '16', '17', '25', '19', '20', '32', '51', '82', '81', '92', '94', '99', '101', '102', '106', '107', '113', '108', '109', '110', '115', '119', '128', '131', '130', '123', '112', '98', '93', '87', '88', '79', '83', '84', '85', '86', '80', '76', '71', '70', '67', '66', '62', '65', '69', '63', '59', '60', '61', '41', '40', '42', '44', '43']
            print(calc_sum_of_path(ans,g.graph_dict))
            print(calc_ham_sum_of_path(ans, g.graph_dict))

            write_results_to_file(output_files_paths[index], ans)

            ans.append(ans[-1])
            draw_graph_from_result(cord, ans, "Simulated Annealing")


if __name__ == '__main__':
    main()
