import tkinter as tk
from graph_canvas import Graph_canvas
from graph_notebook import Graph_notebook

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.menu = self.create_menu()
        self.config(menu=self.menu)
        left = tk.Frame(self, borderwidth=10, relief=tk.SUNKEN)
        right = tk.Frame(self, borderwidth=10, relief=tk.SUNKEN)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.notebooks = Graph_notebook(left), Graph_notebook(right)
        for b in self.notebooks:
            b.pack(fill=tk.BOTH, expand=True)
    
    def create_menu(self):
        menu = tk.Menu(self)
        menu.add_command(label="Изоморфность", command=self.test_equal)
        # menu.add_command(label="Справка")
        return menu
    
    def test_equal(self):
        left = self.notebooks[0].graph
        right = self.notebooks[1].graph
        message = "Графы изоморфны" if left == right else "Графы не изоморны"
        tk.messagebox.showinfo(self, message=message)


if __name__ == '__main__':
    App().mainloop()