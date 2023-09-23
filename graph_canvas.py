from math import dist, pi
import tkinter as tk
from collections import defaultdict
from functools import partial
from itertools import combinations
from random import random, randrange
from cmath import rect

from my_graph import Graph

figID = int

class Vertex:
    def __init__(self, canvas: tk.Canvas, 
                 x: int, y: int):
        self.canvas = canvas
        self.r = 10
        self.oval = canvas.create_oval(x-self.r, y-self.r, x+self.r, y+self.r, 
                                        fill="red", tags="movable")
        self.edges = set()
    
    def add_edge(self, edge: 'Edge'):
        self.edges.add(edge)

    @property
    def center(self) -> tuple[float, float]:
        x0, y0, x1, y1 = self.canvas.coords(self.oval)
        return (x0+x1)/2, (y0+y1)/2
    
    def moveto(self, x: int, y: int):
        self.canvas.moveto(self.oval, x-self.r, y-self.r)
        for edge in self.edges:
            edge.update()


class Edge:
    def __init__(self, canvas: tk.Canvas, 
                 start: Vertex, end: Vertex) -> None:
        self.canvas = canvas
        self.start, self.end = start, end
        self.line = self.canvas.create_line(*self.start.center,
                                            *self.end.center)
    
    def update(self):
        self.canvas.coords(self.line, *self.start.center, *self.end.center)

class Graph_canvas(tk.Canvas):
    def __init__(self, master, graph) -> None:
        self.height, self.width = 400, 400
        super().__init__(master, bg="white", height=self.height, width=self.width)
        
        self.bind("<Button-1>", self.choose)
        self.bind("<ButtonRelease-1>", self.unchoose)
        self.draw_graph(graph)
    
    def draw_graph(self, graph):
        vertices = {}
        for i, vertex in enumerate(graph.keys()):
            xy = rect(self.height//3, i*pi*2/len(graph.keys()))
            x, y = xy.real+self.width//2, xy.imag+self.height//2
            vertices[vertex] = Vertex(self, x, y)

        for k_start in vertices.keys():
            for k_end in graph[k_start]:
                start, end = vertices[k_start], vertices[k_end]
                edge = Edge(self, start, end)
                start.add_edge(edge)
                end.add_edge(edge)
        self.vertices_by_figID = {v.oval: v for v in vertices.values()}
    
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
    matrix = read_adjacency("test3.txt")
    graph = Graph.from_adjacency(matrix)
    canvas = Graph_canvas(root, graph.edges)
    canvas.pack()
    root.mainloop()