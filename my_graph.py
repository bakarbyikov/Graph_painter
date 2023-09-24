from collections import defaultdict
from copy import deepcopy
from functools import partial
from io import StringIO
from itertools import combinations, permutations, product, repeat

from file_parcer import read_adjacency


class Graph:

    def __init__(self, edges: dict[str, dict[str, int]], vertices: set[str]=None):
        self.edges = defaultdict(partial(defaultdict, int))
        self.edges.update(edges)
        for v in vertices or ():
            if v in self.edges:
                continue
            self.edges[v] = self.edges.default_factory()
    
    @classmethod
    def from_adjacency(cls, matrix: list[list[int]]) -> 'Graph':
        edges = defaultdict(partial(defaultdict, int))
        for i, row in enumerate(matrix):
            edges[str(i)] = edges.default_factory()
            for j, value in enumerate(row):
                if value <= 0:
                    continue
                edges[str(i)][str(j)] = value
        return cls(edges)
    
    @property
    def vertices(self) -> list[str]:
        return sorted(self.edges.keys())
    
    @property
    def degree(self) -> dict[str, int]:
        return {k: sum(v.values()) for k, v in self.edges.items()}
    
    def is_correct_nickname(self, nickname: list[str]) -> bool:
        for old, new in zip(self.vertices, nickname):
            if self.degree[old] != self.degree[new]:
                return False
        return True
    
    def rename(self, mapping: dict[str, str]):
        old = deepcopy(self.edges)
        self.edges = defaultdict(partial(defaultdict, int))
        for k1, k2 in product(old.keys(), repeat=2):
            self.edges[mapping[k1]][mapping[k2]] = old[k1][k2]
            if not self.edges[mapping[k1]][mapping[k2]]:
                del self.edges[mapping[k1]][mapping[k2]]
    
    def list_adjacent(self, vertex: str) -> list[str]:
        return [name for name, count in self.edges[vertex].items() if count > 0]
    
    def all_nicknames(self):
        yield from permutations(self.vertices)
    
    def correct_nicknames(self):
        not_degree = defaultdict(set)
        for vertex, degree in self.degree.items():
            not_degree[degree].add(vertex)
        
        data = [self.degree[v] for v in self.vertices]
        for nickname in product(*[not_degree[d] for d in data]):
            if len(set(nickname)) < len(nickname):
                continue
            yield nickname

    def __eq__(self, value: 'Graph') -> bool:
        if len(self.vertices) != len(value.vertices):
            return False
        
        for nickname in self.correct_nicknames():
            self.rename({i: j for i, j in zip(self.vertices, nickname)})
            if self.edges == value.edges:
                return True
        return False
    
        
    def reachability(self) -> list[list[bool]]:
        reachable = defaultdict(set)
        visited = set()
        path = [self.vertices[0]]
        while path:
            current = path[-1]
            reachable[current].add(current)
            visited.add(current)

            for child in self.edges[current].keys():
                if child in visited:
                    reachable[current].update(reachable[child])
                    continue
                reachable[current].add(child)
                path.append(child)
                break
            else:
                path.pop()
        
        return [[int(i in v) for i in self.vertices] for _, v in sorted(reachable.items())]



    def __str__(self) -> str:
        with StringIO() as s:
            for key, value in self.edges.items():
                print(f"{key}: ", end='', file=s)
                for key, count in value.items():
                    print(*repeat(key, count), end=' ', file=s)
                print(file=s)
            return s.getvalue()
        

if __name__ == '__main__':
    matrix = read_adjacency("examples/test3.txt")
    g1 = Graph.from_adjacency(matrix)
    print(len(list(g1.all_nicknames())))
    print(len(list(g1.correct_nicknames())))

