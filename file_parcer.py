from io import TextIOWrapper

from exceptions import BadFile


def read_size(file: TextIOWrapper) -> int:
    line = file.readline()
    try:
        size = int(line)
    except ValueError:
        raise BadFile(f"Некорректный размер матрицы: '{line}'")
    else:
        return size

def read_row(file: TextIOWrapper, n: int, n_parts: int) -> list[int]:
    line = file.readline()
    parts = line.split()
    if len(parts) != n_parts:
        raise BadFile(f"Некорректная длинна строки {n}: "\
                      +f"Ожидалось {n_parts}, получено {len(parts)}")
    result = list()
    for i, raw in enumerate(parts):
        try:
            parsed = int(raw)
        except ValueError:
            raise BadFile(f"Некорректный символ {i} строки {n}: {raw}")
        else:
            result.append(parsed)

def read_adjacency(path: str) -> list[list[int]]:
    with open(path) as file:
        size = read_size(file)
        matrix = [read_row(file, i, size) for i in range(size)]
    return matrix

if __name__ == '__main__':
    print(read_adjacency("examples/empty.txt"))