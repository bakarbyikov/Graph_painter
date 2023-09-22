
def from_adjacency(path: str) -> list[list[int]]:
    with open(path) as file:
        size = int(file.readline())
        matrix = list()
        for _ in range(size):
            row = list(map(int, file.readline().split()))
            assert len(row) == size
            matrix.append(row)
    return matrix