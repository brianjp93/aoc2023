from pathlib import Path
from typing import TypeAlias

data = (Path(__file__).parent.parent / "data" / "day10.txt").read_text()
DIR = ((1, 0), (-1, 0), (0, 1), (0, -1))
POSSIBLE = {
    (1, 0): ({'-', 'F', 'L'}, {'7', '-', 'J'}),
    (-1, 0): ({'7', '-', 'J'}, {'F', '-', 'L'}),
    (0, 1): ({'|', 'F', '7'}, {'L', 'J', '|'}),
    (0, -1): ({'L', 'J', '|'}, {'|', 'F', '7'}),
}
WALL = {
    "L": "7",
    "F": "J",
}

Coord: TypeAlias = tuple[int, int]


def get_adj(coord: Coord):
    for dir in DIR:
        yield (dir[0] + coord[0], dir[1] + coord[1]), dir


class Maze:
    def __init__(self, data: str):
        self.start, self.map, self.x_range, self.y_range = self.parse(data)
        self.calculate_start_character()

    def find_loop(self):
        dmap: dict[Coord, int] = {self.start: 0}
        stack = [self.start]
        while stack:
            coord = stack.pop()
            dist = dmap[coord]
            current_ch = self.map[coord]
            for adj, dir in get_adj(coord):
                ndist = dmap.get(adj, 100000000000000)
                ch = self.map.get(adj, '.')
                current_possible, next_possible = POSSIBLE[dir]
                if current_ch in current_possible and ch in next_possible:
                    if dist + 1 < ndist:
                        stack.append(adj)
                        dmap[adj] = dist + 1
        return dmap

    def find_inner(self):
        loop = set(self.find_loop().keys())
        flooded: set[Coord] = set()
        for coord in loop:
            for adj, _ in get_adj(coord):
                if adj in flooded or adj in loop or not self.is_inside_loop(adj, loop):
                    continue
                flooded |= self.flood(adj, loop)
        return flooded

    def calculate_start_character(self):
        pipes = {'|', 'F', 'L', '7', 'J', '-'}
        for adj, dir in get_adj(self.start):
            from_possible, to_possible = POSSIBLE[dir]
            ch = self.map.get(adj, "")
            if ch in to_possible:
                pipes &= from_possible
        char = pipes.pop()
        self.map[self.start] = char
        return char

    def is_inside_loop(self, coord: Coord, loop: set[Coord]):
        count = 0
        x = 0
        while x <= coord[0]:
            ncoord = (x, coord[1])
            if ncoord in loop:
                ch = self.map[ncoord]
                if ch == '|':
                    count += 1
                elif ch in ('F', 'L'):
                    ncoord = self.get_matching(ncoord)
                    if ncoord:
                        other_ch = self.map[ncoord]
                        x = ncoord[0] + 1
                        if other_ch == WALL[ch]:
                            count += 1
                        continue
            x += 1
        return count % 2 == 1

    def get_matching(self, coord: Coord):
        while True:
            coord = (coord[0] + 1, coord[1])
            ch = self.map.get(coord, "")
            if ch == "-":
                continue
            elif ch in ("J", "7"):
                return coord
            else:
                return False

    def flood(self, coord: Coord, loop: set[Coord]):
        flooded = {coord}
        stack = [coord]
        while stack:
            coord = stack.pop()
            for adj, _ in get_adj(coord):
                if adj in flooded:
                    continue
                if adj in loop:
                    continue
                flooded.add(adj)
                stack.append(adj)
        return flooded

    @staticmethod
    def parse(data):
        m: dict[Coord, str] = {}
        start: Coord = (0, 0)
        lines = data.splitlines()
        y_range = (0, len(lines))
        x_range = (0, len(lines[0]))
        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                m[(x, y)] = ch
                if ch == 'S':
                    start = (x, y)
        return start, m, x_range, y_range


if __name__ == '__main__':
    maze = Maze(data)
    dist = maze.find_loop()
    x = max(dist.items(), key=lambda x: x[1])[1]
    print(x)
    inner = maze.find_inner()
    print(len(inner))
