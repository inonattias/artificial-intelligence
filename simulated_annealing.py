from typing import List, Tuple

import numpy

from tspAnnealingProblem import TSPAnnealingProblem
from utils import probability
import numpy as np

max_iter = 100000


def schedule_alpha(t0=1e10, alpha=0.996, limit=100000):
    return lambda t: ((t0 * np.power(alpha, t)) if t < limit else 0)


def schedule_beta(t0=1e10, beta=10.0, limit=100000):
    return lambda t: ((t0 / (1 + beta * t)) if t < limit else 0)


def simulated_annealing1(problem: TSPAnnealingProblem, schedule=schedule_alpha()):
    current_state: Tuple[List[str], float] = problem.initial
    for t in range(max_iter):
        swapped: bool = False
        T: float = schedule(t)
        if T < np.exp(-800) or T == 0.0:
            return current_state[0], problem.calc_hamilton_path_len(current_state)

        next_state: Tuple[List[str], float] = problem.get_random_next_state(current_state)
        value_diff = current_state[1] - next_state[1]

        prob = np.exp(value_diff / T)

        if value_diff > 0.0 or probability(prob):
            current_state = next_state
            swapped = True
        hamiltonCircle = problem.calc_hamilton_path_len(current_state)

        print(
            "iteration: {iter}. Temp. = {T}. diff = {value_diff}. swapped= {swapped}. probability = {prob}. tsp length: {length}. hammCircle: {hamCir}".format
            (iter=t, T=T, value_diff=value_diff, swapped=swapped, prob=prob, length=current_state[1],
             hamCir=hamiltonCircle))
    return current_state[0], problem.calc_hamilton_path_len(current_state)


def get_best_alpha_params(problem: TSPAnnealingProblem, init_temp: List[float], alphas: List[float], max_iter):
    results = []
    t0_results = []

    for t0 in init_temp:
        for alpha in alphas:
            sum = 0.0
            for i in range(0, max_iter):
                sum += simulated_annealing1(problem, schedule=schedule_alpha(t0=t0, alpha=alpha))[1]

            path_avg = sum / max_iter
            results.append(path_avg)
        t0_results.append(results)
    for index1, t0_result in enumerate(t0_results):
        t0 = init_temp[index1]
        for index, alpha in enumerate(alphas):
            print("t0:{t0}, alpha: {alpha}, tsp average length of path: {path_avg} for {maxIter} runs".format(t0=t0,
                                                                                                              alpha=alpha,
                                                                                                              path_avg=
                                                                                                              t0_results[
                                                                                                                  index1][index],
                                                                                                              maxIter=max_iter))


def get_best_beta_params(problem: TSPAnnealingProblem, init_temp: List[float], betas: List[float], max_iter):
    results = []
    t0_results = []
    min = 1e10
    min_path = []
    for t0 in init_temp:
        for beta in betas:
            sum = 0.0
            for i in range(0, max_iter):
                path, path_len= simulated_annealing1(problem, schedule=schedule_beta(t0 = t0, beta=beta))
                sum += path_len
                if path_len< min:
                    min = path_len
                    min_path = path
            path_avg = sum / max_iter
            results.append(path_avg)

        t0_results.append(results)
    for index1, t0_result in enumerate(t0_results):
        t0 = init_temp[index1]
        for index, beta in enumerate(betas):
                print("t0:{t0}, beta: {beta}, tsp average length of path: {path_avg} for {maxIter} runs".format(t0=t0,
                                                                                                                beta=beta,
                                                                                                   path_avg=t0_results[
                                                                                                       index1][index],
                                                                                                   maxIter=max_iter))
    print(min_path)
    print(min)
    return min_path
