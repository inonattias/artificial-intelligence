from tkinter import *
from typing import Tuple, List


def draw_graph(path: Tuple[Tuple[float, float]], labels: List[str]):
    assert len(path) == len(labels)
    factor = 3.0
    adjusted_path = tuple([(e[0]*factor, e[1]*factor) for e in path])

    root = Tk()
    root.title("Map of path in Graph")

    width = 800
    height = 400
    margin = 3.0
    y_label_margin = -5 * factor
    label_margin = -4* factor
    graph_map = Canvas(root, width=width, height=height)
    graph_map.configure(scrollregion=(-400, -400, 200, 200))


    graph_map.pack()

    for index, node in enumerate(adjusted_path):

        if index == len(labels) - 1:
            graph_map.create_line(node[0], node[1], adjusted_path[0][0], adjusted_path[0][1],
                                  fill="red", width=3)
        else:
            graph_map.create_line(node[0], node[1], adjusted_path[index + 1][0], adjusted_path[index + 1][1],
                                  fill="red", width=3)

    for index, label in enumerate(labels):
        label_coord = adjusted_path[index][0] - margin, adjusted_path[index][1] + margin, adjusted_path[index][0] + margin, adjusted_path[index][1] - margin
        graph_map.create_text(adjusted_path[index][0]+ label_margin, adjusted_path[index][1] - y_label_margin, anchor=W, font="Purisa", text=label)
        graph_map.create_oval(label_coord, fill="green")


    graph_map.pack()

    root.mainloop()


def _test():
    draw_graph(((1, 1), (2, 1), (2, 2), (1, 2), (0.5, 1.5)), ['1', '3', '4', '6', '9'])


if __name__ == '__main__':
    _test()
