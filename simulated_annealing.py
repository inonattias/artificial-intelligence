from typing import List, Tuple

from tspAnnealingProblem import TSPAnnealingProblem
from utils import probability
import numpy as np

max_iter = 5000


def exp_schedule(t0=20, alpha=0.005, limit=100):
    return lambda t: ((t0 * np.power(alpha, t)) if t < limit else 0)


def simulated_annealing(problem: TSPAnnealingProblem, schedule=exp_schedule()):
    current_state: Tuple[List[str], float] = problem.initial
    for t in range(max_iter):
        swapped: bool = False
        T: float = schedule(t)
        if T == 0:
            return current_state

        next_state: Tuple[List[str], float] = problem.get_random_next_state(current_state)
        value_diff = current_state[1] - next_state[1]

        prob = np.exp(value_diff / T)

        if value_diff > 0.0 or probability(prob):
            current_state = next_state
            swapped = True
        print("iteration: {iter}. Temp. = {T}. diff = {value_diff}. swapped= {swapped}. probability = {prob}".format
              (iter=t, T=T, value_diff=value_diff, swapped=swapped, prob=prob))
    return current_state
