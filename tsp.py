import random
from tkinter import *
from tkinter import messagebox

import utils
from search import *
from typing import Tuple

distances = {}


# romania_problem = GraphProblem('Arad', 'Bucharest', romania_map)

class TSProblem(Problem):
    """subclass of Problem to define various functions"""

    # מצב התחלתי: גרף הכולל n קודקודים, ללא אף קשת. אופרטורים: הוספת קשת למצב, באופן שתייצר מסלול. (לאחר שיש n-1 קשתות - נוסיף עוד אופרטור שיסגור את המעגל ההמילטוני)
    # עלות אופרטור: אורך הקשת שהוספנו. מבחן יעד: מעגל המילטוני (n קשתות)
    # אם כך, מצבי הביניים יהיו כל המצבים ש"בין" המצב ההתחלתי למצב היעד, כלומר מצבים שבהם יש מסלול הכולל בין 1 ל n-1 קשתות)

    def __init__(self, graph: Graph):
        super().__init__(initial=(graph.graph_dict, []))
        assert not graph.directed
        self.graph: Dict[str, Dict[str, float]] = graph.graph_dict
        self.number_of_vertices = graph.number_of_vertices
        self.path_so_far_state: List[str] = []  # state

    def goal_test(self, state):
        return len(set(state)) == self.number_of_vertices and \
               len(state) == len(set(state)) and \
               state[0] == state[self.number_of_vertices - 1]

    def actions(self, path_so_far: List[str]) -> List[str]:
        return list(filter(lambda x: x not in path_so_far, self.graph.get(path_so_far[-1]).keys()))


    def __check_action_is_valid(self, path_so_far: List[str], action: str) -> bool:
        return action in self.actions(path_so_far)

    def result(self, path_so_far: List[str], action: str):
        if not self.__check_action_is_valid(path_so_far, action):
            raise RuntimeWarning('action' + action + 'is not valid ')
        path_so_far.append(action)

    def path_cost(self, path_so_far: List[str]) -> float:
        cost: float = 0.0
        for index, v in enumerate(path_so_far):
            if index < len(path_so_far):
                cost += self.graph.get(v, path_so_far[index + 1])
        return cost

    def path_cost(self, cost_so_far, A: str, B: str):
        if not self.graph.get(A, B):
            raise RuntimeWarning('action' + A + ' to ' + B + 'is not valid ')
        return cost_so_far + (self.graph.get(A, B) or np.inf)

    def value(self, path_so_far: List[str]) -> float:
        """value of path cost given negative for the given state"""
        return self.path_cost(path_so_far)


if __name__ == '__main__':
    pass
