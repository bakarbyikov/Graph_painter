from collections import defaultdict
from functools import partial
from io import StringIO
from itertools import permutations, product
from math import isnan
from typing import Generator, Literal

from file_parcer import read_adjacency


class Graph:

    def __init__(self):
        self.edges = defaultdict(partial(defaultdict, partial(defaultdict, int)))
        self.edges: dict[str, dict[str, dict[int|float, float]]]
    
    def add_vertex(self, name: str):
        assert isinstance(name, str)
        self.edges[name] = self.edges.default_factory()
    
    def add_edge(self, start: str, end: str, 
                 weight: int|float=0, count=1):
        assert isinstance(start, str) and isinstance(end, str)
        self.edges[start][end][weight] += count
    
    def set_edge(self, start: str, end: str, 
                 edge: dict[int|float, float]):
        assert isinstance(start, str) and isinstance(end, str)
        self.edges[start][end].update(edge)
    
    @classmethod
    def from_weights(cls, matrix: list[list[int|float|None]]) -> 'Graph':
        graph = cls()
        for start, row in enumerate(matrix):
            graph.add_vertex(str(start))
            for end, value in enumerate(row):
                if value is None or isnan(value):
                    continue
                graph.add_edge(str(start), str(end), weight=value)
        return graph
    
    @classmethod
    def from_adjacency(cls, matrix: list[list[int]]) -> 'Graph':
        graph = cls()
        for start, row in enumerate(matrix):
            graph.add_vertex(str(start))
            for end, value in enumerate(row):
                if value <= 0:
                    continue
                graph.add_edge(str(start), str(end), count=value)
        return graph
    
    @classmethod
    def from_incidence(cls, matrix: list[list[int|float]], 
                       stored_data: Literal["count", "weight"]="count") -> 'Graph':
        graph = cls()
        for row in matrix:
            value = max(row)
            start, end = row.index(value), row.index(-value)
            match stored_data:
                case "count":
                    graph.add_edge(str(start), str(end), count=value)
                case "weight":
                    graph.add_edge(str(start), str(end), weight=value)
                case _:
                    raise TypeError(f"{stored_data} is an invalid keyword "\
                                    +"argument for stored_data")
        return graph
    
    
    def vertices(self) -> set[str]:
        return set(self.edges.keys())
    
    def list_adjacent(self, vertex: str) -> set[str]:
        return set(self.edges[vertex].keys())
    
    def degree(self) -> dict[str, int]:
        result = defaultdict(int)
        for start in self.vertices():
            result[start] = 0
            for end in self.list_adjacent(start):
                result[start] += sum(self.edges[start][end].values())
        return result

    def weights(self, start: str, end: str) -> set[int|float]:
        return set(self.edges[start][end].keys())
    
    def min_spanning_tree(self, start: str=None):
        if start is None:
            start = self.vertices().pop()
        assert start in self.vertices()
        tree = Graph()
        chosed = set(start)
        while True:
            vertex = None, None
            min_weight = None
            for begin in chosed:
                for end in self.list_adjacent(begin)-chosed:
                    weight = min(self.weights(begin, end))
                    if min_weight is None or weight < min_weight:
                        vertex = begin, end
                        min_weight = weight
            if min_weight is None:
                break
            chosed.add(vertex[-1])
            tree.add_edge(*vertex, weight=min_weight)
            tree.add_edge(*vertex[::-1], weight=min_weight)
        return tree
    
    def rename(self, mapping: dict[str, str]):
        renamed = Graph()
        for start in self.vertices():
            new_start = mapping[start]
            for end in self.list_adjacent(start):
                edge = self.edges[start][end]
                new_end = mapping[end]
                renamed.set_edge(new_start, new_end, edge)
        self.edges = renamed.edges
    
    def all_nicknames(self) -> Generator[tuple[str], None, None]:
        yield from permutations(self.vertices())
    
    def correct_nicknames(self) -> Generator[tuple[str], None, None]:
        vertecies_by_degree = defaultdict(set)
        for vertex, degree in self.degree().items():
            vertecies_by_degree[degree].add(vertex)
        
        degree_list = [self.degree()[v] for v in sorted(self.vertices())]
        for nickname in product(*[vertecies_by_degree[d] for d in degree_list]):
            if len(set(nickname)) < len(nickname):
                continue
            yield nickname

    def __eq__(self, value: 'Graph') -> bool:
        if len(self.vertices()) != len(value.vertices()):
            return False
        
        for nickname in self.correct_nicknames():
            self.rename({i: j for i, j in zip(sorted(self.vertices()), nickname)})
            if self.edges == value.edges:
                return True
        return False
        
    def reachability(self) -> dict[str, set[str]]:
        reachable = defaultdict(set)
        visited = set()
        path = list(self.vertices())
        while path:
            current = path[-1]
            reachable[current].add(current)
            visited.add(current)

            for child in self.list_adjacent(current):
                if child in visited:
                    reachable[current].update(reachable[child])
                    continue
                reachable[current].add(child)
                path.append(child)
                break
            else:
                path.pop()
        return reachable

    def __str__(self) -> str:
        with StringIO() as s:
            for start in sorted(self.vertices()):
                print(f"{start}: ", end='', file=s)
                for end in self.list_adjacent(start):
                    print(f"{end}={dict(self.edges[start][end])}", end=' ', file=s)
                print(file=s)
            return s.getvalue()
        

if __name__ == '__main__':
    matrix = read_adjacency("examples/test3.txt")
    g1 = Graph.from_adjacency(matrix)
    print(g1)
    print(g1.reachability())
    print(len(list(g1.all_nicknames())))
    print(len(list(g1.correct_nicknames())))

