from tkinter import *
from typing import Tuple, List


class Gui():
    def __init__(self, path: Tuple[Tuple[float, float]], labels: List[str], algo_name: str):
        assert len(path) == len(labels)
        self.labels: List[str] = labels
        self.root = Tk()
        self.path: Tuple[Tuple[float, float]] = path
        self.canvas_width: float = 0.0
        self.canvas_height: float = 0.0
        self.cord_locations: List[Tuple[float, float]] = list(path)
        self.calculate_canvas_size()

        self.frame_select_cities = Frame(self.root)
        self.frame_select_cities.grid(row=1)
        self.frame_canvas = Frame(self.root)
        self.frame_canvas.grid(row=2)
        Label(self.root, text="Graph of TSP for " + algo_name, font="Times 13 bold").grid(row=0, columnspan=10)

    def calculate_canvas_size(self):
        """Width and height for canvas"""

        minx, maxx = sys.maxsize, -1 * sys.maxsize
        miny, maxy = sys.maxsize, -1 * sys.maxsize

        for cord in self.path:
            minx = min(minx, cord[0])
            maxx = max(maxx, cord[0])
            miny = min(miny, cord[1])
            maxy = max(maxy, cord[1])
        if minx >=0:
            minx = -1
        if miny >= 0:
            miny = -1
        diff_x: float = maxx - minx
        factor_x = (18.5 - diff_x / 10)
        diff_y: float = maxy - miny
        factor_y = (15 - diff_y / 10)

        # New locations squeezed to fit inside the map of romania
        for index, cor in enumerate(list(self.path)):
            self.cord_locations[index] = (
                (cor[0] * factor_x / 1.2) - minx * factor_x / 1.1 + 20, -cor[1] * factor_y / 1.2 + miny*factor_y/1.2 + 430)

        print(self.cord_locations)
        print(self.path)
        print(minx)
        print(miny)
        canvas_width = (maxx - minx) + 630
        canvas_height = (maxy - miny) + 400

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

    def draw_graph(self):
        margin = 3
        adjusted_path = self.cord_locations

        self.root.title("Map of path in Graph")

        graph_map = Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        graph_map.grid(row=3, columnspan=10)

        for index, node in enumerate(adjusted_path):

            if index == len(self.labels) - 1:
                graph_map.create_line(node[0], node[1], adjusted_path[0][0], adjusted_path[0][1],
                                      fill="red", width=3)
            else:
                graph_map.create_line(node[0], node[1], adjusted_path[index + 1][0], adjusted_path[index + 1][1],
                                      fill="red", width=3)

        for index, label in enumerate(self.labels):
            label_coord = adjusted_path[index][0] - margin, adjusted_path[index][1] + margin, adjusted_path[index][
                0] + margin, adjusted_path[index][1] - margin
            graph_map.create_text(adjusted_path[index][0] - 15, adjusted_path[index][1] - 10, anchor=W, font="Purisa 8",
                                  text=label)
            graph_map.create_oval(label_coord, fill="green")
        self.root.mainloop()


def _test():
    g = Gui(((0, 1), (2, 10), (2, 20), (1, 2), (14.5, 22.5)), ['1', '3', '4', '6', '9'], "TEST")
    g.draw_graph()


if __name__ == '__main__':
    _test()
