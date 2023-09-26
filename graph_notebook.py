from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import Literal
from exceptions import BadFile
from graph_canvas import Graph_canvas
from file_parcer import read_adjacency, read_weighted

from my_graph import Graph
from custom_notebook import CustomNotebook


class Graph_opener(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        tk.Button(self, text="Открыть матрицу смежности", command=self.open_adj).pack()
        tk.Button(self, text="Открыть матрицу весов", command=self.open_weight).pack()
    
    def open_adj(self):
        path = filedialog.askopenfilenames(initialdir=".")[0]
        self.master.open(path, "adj")
    
    def open_weight(self):
        path = filedialog.askopenfilenames(initialdir=".")[0]
        self.master.open(path, "weight")


class Graph_notebook(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.notebook = CustomNotebook(self, height=400, width=400)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        open_graph = Graph_opener(self)
        open_graph.pack(fill=tk.BOTH, expand=True)

        self.notebook.add(open_graph, text="+")
    
    def open_graph(self, path: str, how: Literal['adj', 'weight']) -> Graph:
        match how:
            case 'adj':
                matrix = read_adjacency(path)
                graph = Graph.from_adjacency(matrix)
            case "weight":
                matrix = read_weighted(path)
                graph = Graph.from_weights(matrix)
        return graph
    
    def open(self, path: str, how: Literal['adj', 'weight']):
        try:
            self.graph = self.open_graph(path, how)
        except BadFile as e:
            tk.messagebox.showerror(title=e.__doc__, message=e)
            raise
        canvas = Graph_canvas(self.notebook, self.graph)
        canvas.pack(fill=tk.BOTH, expand=True)
        name = Path(path).name

        self.notebook.add(canvas, text=name)
        self.notebook.select(self.notebook.tabs()[-1])
        



if __name__ == '__main__':
    root = tk.Tk()
    g = Graph_notebook(root)
    g.pack(fill=tk.BOTH, expand=True)
    root.mainloop()