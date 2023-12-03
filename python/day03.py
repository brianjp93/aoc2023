from pathlib import Path
from dataclasses import dataclass, field
from typing import LiteralString

data = (Path(__file__).parent.parent / "data" / "day03.txt").read_text()
data = data.splitlines()

ADJ = [(1, 1), (1, 0), (0, 1), (-1, -1), (-1, 0), (0, -1), (1, -1), (-1, 1)]


@dataclass
class Map:
    map: list[str | LiteralString]
    found_numbers: set[tuple[int, int]] = field(default_factory=set)

    def get(self, x, y):
        try:
            return self.map[y][x]
        except IndexError:
            return "."

    def get_adj(self, x, y):
        for nx, ny in ADJ:
            newx, newy = x + nx, y + ny
            yield (newx, newy), self.get(newx, newy)

    def find_adj_number(self, x, y):
        for (nx, ny), adj in self.get_adj(x, y):
            if adj.isdigit():
                lx = nx
                mx = nx
                while self.get(lx - 1, ny).isdigit():
                    lx -= 1
                while self.get(mx + 1, ny).isdigit():
                    mx += 1
                num = int(self.map[ny][lx:mx + 1])
                if (lx, ny) not in self.found_numbers:
                    self.found_numbers.add((lx, ny))
                    yield num

    def find_2_adj_numbers(self, x, y):
        adj = list(self.find_adj_number(x, y))
        if len(adj) == 2:
            return adj
        return []

    def is_symbol(self, x, y):
        ch = self.get(x, y)
        if ch.isdigit() or ch == ".":
            return False
        return True

    def is_gear(self, x, y):
        return self.get(x, y) == '*'

    def find_part_numbers(self):
        for y, row in enumerate(self.map):
            for x in range(len(row)):
                if self.is_symbol(x, y):
                    for num in self.find_adj_number(x, y):
                        yield num

    def find_gear_ratios(self):
        for y, row in enumerate(self.map):
            for x in range(len(row)):
                if self.is_gear(x, y):
                    if adj := self.find_2_adj_numbers(x, y):
                        yield adj[0] * adj[1]


if __name__ == '__main__':
    map = Map(map=data)
    print(sum(map.find_part_numbers()))
    map.found_numbers = set()
    print(sum(map.find_gear_ratios()))
