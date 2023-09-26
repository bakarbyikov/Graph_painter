import tkinter as tk
from  tkinter import ttk

class Table_window(tk.Toplevel):

    def __init__(self, master, table: list[list[int]], title: str):
        super().__init__(master)
        self.title(title)

        self.create_table(table).pack()
    
    def create_table(self, table: list[list[int]]) -> ttk.Treeview:
        columns = [f"#{i+1}" for i in range(len(table[0]))]
        tree = ttk.Treeview(self, show="headings", columns=columns, padding=0)
        for i, name in enumerate(table[0]):
            tree.heading(f"#{i+1}", text=name)
            tree.column(f"#{i+1}", width=20)
        
        for row in table[1:]:
            tree.insert("", tk.END, values=row)
        return tree

def show_table(table: list[list[int]], title=''):
    Table_window(None, table, title)

if __name__ == '__main__':
    from random import *
    root = tk.Tcl()
    table = [choices(range(10), k=10) for _ in range(10)]
    show_table('table', table)
    root.mainloop()

    