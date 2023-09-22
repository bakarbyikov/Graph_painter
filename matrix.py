from io import StringIO
from itertools import combinations
import sys


class Matrix:

    def __init__(self) -> None:
        self.size = self.input_size()
        self.matrix = self.input_matrix()

    @classmethod
    def from_file(cls, file):
        inp_stream = sys.stdin
        with open(file) as f:
            sys.stdin = StringIO(f.read())
        m = cls()
        sys.stdin = inp_stream
        return m

    def input_size(self):
        while True:
            line = input("Введите кол-во вершин: ")
            try:
                size = int(line)
            except ValueError:
                print(f"Введенная строка {line} не является числом.")
                continue
            if size <= 0:
                print("Число вершин должно быть больше нуля.")
                continue
            return size

    def input_row(self, row_number: int):
        while True:
            print("\n ", *range(1, self.size+1))
            line = input(f"{row_number} ")
            row = []
            for i, v in enumerate(line.split()):
                try:
                    row.append(int(v))
                except  ValueError:
                    print(f"Введенная символ в позиции {i} не является числом.")
                    continue
            if len(row) != self.size:
                print(f"Введеная строка длинны {len(row)}, ожидалось {self.size}")
            return row

    def input_matrix(self):
        matrix = []
        for i in range(self.size):
            matrix.append(self.input_row(i+1))
        return matrix
    
    def __str__(self):
        with StringIO() as s:
            print(self.size, file=s)
            for row in self.matrix:
                print(*row, file=s)
            text = s.getvalue()
        return text
    
    def swap(self, i: int, j: int):
        self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]
        for row in self.matrix:
            row[i], row[j] = row[j], row[i]
    
    def __eq__(self, __value: 'Matrix') -> bool:
        if self.size != __value.size:
            return False
        
        for i, j in combinations(range(self.size), 2):
            self.swap(i, j)
            if self.matrix == __value.matrix:
                return True
            self.swap(i, j)
        
        return False

if __name__ == '__main__':
    print(Matrix())