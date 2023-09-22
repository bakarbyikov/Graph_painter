from math import pi
import tkinter as tk
from collections import defaultdict
from functools import partial
from itertools import combinations
from random import random, randrange
from cmath import rect

from my_graph import Graph


class Vertex:
    def __init__(self, canvas: tk.Canvas, 
                 x: int, y: int, r: int=10):
        self.canvas = canvas
        self.r = r
        self.figID = canvas.create_oval(x-r, y-r, x+r, y+r, fill="red")
        self.edges = set()
    
    def add_edge(self, edge: 'Edge'):
        self.edges.add(edge)

    @property
    def center(self) -> tuple[float, float]:
        x0, y0, x1, y1 = self.canvas.coords(self.figID)
        return (x0+x1)/2, (y0+y1)/2
    
    def moveto(self, x: int, y: int):
        self.canvas.moveto(self.figID, x-self.r, y-self.r)
        for edge in self.edges:
            edge.update()


class Edge:
    def __init__(self, canvas: tk.Canvas, 
                 start: Vertex, end: Vertex) -> None:
        self.canvas = canvas
        self.start, self.end = start, end
        self.figID = self.canvas.create_line(*self.start.center, 
                                             *self.end.center, 
                                             tags="static")
    
    def update(self):
        self.canvas.coords(self.figID, *self.start.center, *self.end.center)

class Graph_canvas(tk.Canvas):
    def __init__(self, master, graph) -> None:
        self.height, self.width = 400, 400
        super().__init__(master, bg="white", height=self.height, width=self.width)
        
        self.bind("<Button-1>", self.choose)
        self.draw_graph(graph)
    
    def draw_graph(self, graph):
        r = 10
        vertices = {}
        for i, vertex in enumerate(graph.keys()):
            xy = rect(self.height//3, i*pi*2/len(graph.keys()))
            x, y = xy.real+self.width//2, xy.imag+self.height//2
            vertices[vertex] = Vertex(self, x, y, r)

        for k_start in vertices.keys():
            for k_end in graph[k_start]:
                start, end = vertices[k_start], vertices[k_end]
                edge = Edge(self, start, end)
                start.add_edge(edge)
                end.add_edge(edge)
        self.vertices_by_figID = {v.figID: v for v in vertices.values()}

    def update(self, vertex: Vertex, event):
        vertex.moveto(event.x, event.y)

    def choose(self, event):
        finded = self.find_closest(event.x, event.y, 10, 'static')
        vertex = self.vertices_by_figID[finded[0]]
        self.bind("<B1-Motion>", partial(self.update, vertex))



if __name__ == "__main__":
    root = tk.Tk()
    g = Graph_canvas(root)
    g.pack()
    
    matrix = [[0, 1, 1, 1],
              [1, 0, 0, 1],
              [1, 0, 0, 0],
              [1, 1, 0, 0]]
    
    g.draw_graph(Graph.from_adjacency(matrix).edges)
    root.mainloop()