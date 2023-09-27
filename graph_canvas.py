from io import StringIO
import tkinter as tk
from tkinter import messagebox
from cmath import rect
from functools import partial
from math import atan2, cos, dist, pi, sin

from my_graph import Graph
from widgets import show_table

figID = int

class Vertex:
    def __init__(self, canvas: tk.Canvas, name: str):
        self.canvas = canvas
        self.r = 20
        self.oval = canvas.create_oval(-self.r, -self.r, self.r, self.r, 
                                        fill="red", tags="movable")
        self.text = canvas.create_text(0, 0, text=name,
                                       width=self.r*2,
                                       font=('Helvetica', '20'))
        
        x1, y1, x2, y2 = self.canvas.bbox(self.text)
        self.text_offset = (x2-x1)/2, (y2-y1)/2
        self.edges = set()
    
    def add_edge(self, edge: 'Edge'):
        self.edges.add(edge)

    @property
    def center(self) -> tuple[float, float]:
        x0, y0, x1, y1 = self.canvas.coords(self.oval)
        return (x0+x1)/2, (y0+y1)/2
    
    def moveto(self, x: int, y: int):
        self.canvas.moveto(self.oval, x-self.r, y-self.r)
        self.canvas.moveto(self.text, x-self.text_offset[0], y-self.text_offset[1])
        for edge in self.edges:
            edge.update()

class Edge:
    def __init__(self, canvas: tk.Canvas, 
                 start: Vertex, end: Vertex) -> None:
        self.canvas = canvas
        self.start, self.end = start, end
        self.line = self.canvas.create_line(0, 0, 0, 0,
                                            arrow=tk.LAST,
                                            arrowshape=(16,20,6))
    
    def offset(self, start: Vertex, end: Vertex) -> tuple[float, float, float, float]:
        (x1, y1), (x2, y2) = start.center, end.center
        angle = atan2((y2-y1), (x2-x1))
        r1, r2 = start.r, end.r
        c, s = cos(angle), sin(angle)
        return (x1+c*r1, y1+s*r1,
                x2-c*r2, y2-s*r2)
    
    def update(self):
        self.canvas.coords(self.line, *self.offset(self.start, self.end))

class Graph_canvas(tk.Canvas):
    def __init__(self, master, graph: Graph) -> None:
        self.height, self.width = 400, 400
        super().__init__(master, bg="white", height=self.height, width=self.width)
        self.graph = graph
        
        self.bind("<Button-1>", self.choose)
        self.bind("<ButtonRelease-1>", self.unchoose)
        self.draw_graph(graph)
        self.create_menu()
    
    def create_menu(self):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Матрица достижимости", 
                              command=self.show_reachability)
        menu.add_command(label="Оставное дерево Прима", 
                              command=self.spanning_tree)
        
        def do_popup(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
        
        self.bind("<Button-3>", do_popup)
    
    def spanning_tree(self):
        tree = self.graph.min_spanning_tree()
        self.master.add_tab(tree, "Spanning tree")

    def show_reachability(self):
        reachability = self.graph.reachability()
        
        table = list()
        table.append(['',] + sorted(self.graph.vertices()))
        for start in table[0][1:]:
            table.append([start])
            for end in table[0][1:]:
                table[-1].append(int(end in reachability[start]))
        
        show_table(table, "Матрица достижимости")
    
    def reset_positions(self):
        n_vertices = len(self.vertices_by_figID.keys())
        for i, vertex in enumerate(self.vertices_by_figID.values()):
            xy = rect(self.height//3, i*pi*2/n_vertices-pi/2)
            x, y = xy.real+self.width//2, xy.imag+self.height//2
            vertex.moveto(x, y)
    
    def draw_graph(self, graph: Graph):
        vertices = {}
        for vertex in sorted(graph.vertices()):
            vertices[vertex] = Vertex(self, vertex)
        self.vertices_by_figID = {v.oval: v for v in vertices.values()}

        for k_start in vertices.keys():
            for k_end in graph.list_adjacent(k_start):
                start, end = vertices[k_start], vertices[k_end]
                edge = Edge(self, start, end)
                start.add_edge(edge)
                end.add_edge(edge)
        self.reset_positions()
    
    def dist(self, point: tuple[int, int], figure: figID) -> float:
        x1, y1, x2, y2 = self.bbox(figure)
        center = (x1+x2)/2, (y1+y2)/2
        return dist(center, point)
    
    def find_target(self, x: float, y: float) -> figID:
        halo = 5
        finded = self.find_overlapping(x-halo, y-halo,
                                       x+halo, y+halo)
        movable = set(finded) & set(self.find_withtag("movable"))
        if not movable:
            return None
        nearest = min(movable, key=partial(self.dist, (x, y)))
        return nearest
    
    def update(self, vertex: Vertex, event):
        vertex.moveto(event.x, event.y)

    def unchoose(self, event):
        self.unbind("<B1-Motion>")

    def choose(self, event):
        target = self.find_target(event.x, event.y)
        if target is None:
            return
        vertex = self.vertices_by_figID[target]
        self.update(vertex, event)
        self.bind("<B1-Motion>", partial(self.update, vertex))



if __name__ == "__main__":
    from file_parcer import read_adjacency

    root = tk.Tk()
    matrix = read_adjacency("examples/test3.txt")
    graph = Graph.from_adjacency(matrix)
    print(graph)
    canvas = Graph_canvas(root, graph)
    canvas.pack()
    root.mainloop()