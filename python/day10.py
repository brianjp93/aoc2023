from pathlib import Path
from typing import TypeAlias

data = (Path(__file__).parent.parent / "data" / "day10.txt").read_text()


DIR = ((1, 0), (-1, 0), (0, 1), (0, -1))

POSSIBLE = {
    (1, 0): ({'-', 'F', 'L', 'S'}, {'7', '-', 'J'}),
    (-1, 0): ({'7', '-', 'J', 'S'}, {'F', '-', 'L'}),
    (0, 1): ({'|', 'F', '7', 'S'}, {'L', 'J', '|'}),
    (0, -1): ({'L', 'J', '|', 'S'}, {'|', 'F', '7'}),
}

Coord: TypeAlias = tuple[int, int]

WALL = {
    "L": "7",
    "F": "J",
}


def get_adj(coord: Coord):
    for dir in DIR:
        yield (dir[0] + coord[0], dir[1] + coord[1]), dir


class Maze:
    def __init__(self, data: str):
        self.start, self.map, self.x_range, self.y_range = self.parse(data)

    def explore(self):
        dist: dict[Coord, int] = {self.start: 0}
        stack = [self.start]
        while stack:
            coord = stack.pop()
            current_dist = dist[coord]
            current_ch = self.map[coord]
            for adj, dir in get_adj(coord):
                ndist = dist.get(adj, 100000000000000)
                ch = self.map.get(adj, '.')
                current_possible, next_possible = POSSIBLE[dir]
                if current_ch in current_possible and ch in next_possible:
                    if current_dist + 1 < ndist:
                        stack.append(adj)
                        dist[adj] = current_dist + 1
        return dist

    def find_inner(self):
        loop = set(self.explore().keys())
        flooded: set[Coord] = set()
        valid: set[Coord] = set()
        for coord in loop:
            for adj, _ in get_adj(coord):
                if adj in flooded or adj in loop:
                    continue
                if not self.raycast(adj, loop):
                    continue
                # print(f"flooding at {adj=}")
                is_valid, new_valid, new_flooded = self.flood(adj, loop)
                flooded |= new_flooded
                if is_valid:
                    valid |= new_valid
        return valid

    def raycast(self, coord: Coord, loop: set[Coord]):
        count = 0
        x = 0
        while x <= coord[0]:
            ncoord = (x, coord[1])
            if ncoord in loop:
                ch = self.map[ncoord]

                # TODO: make it so we can calculate what S actually is
                if ch == 'S':
                    ch = 'L'

                if ch == '|':
                    count += 1
                elif ch in ('F', 'L'):
                    ncoord = self.get_connector(ncoord)
                    if ncoord:
                        other_ch = self.map[ncoord]
                        x = ncoord[0] + 1
                        if other_ch == WALL[ch]:
                            count += 1
                        continue
            x += 1
        return count % 2 == 1

    def get_connector(self, coord: Coord):
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
        valid = {coord}
        stack = [coord]
        is_valid = True
        while stack:
            coord = stack.pop()
            for adj, _ in get_adj(coord):
                if adj in flooded:
                    continue
                if adj in loop:
                    continue
                ch = self.map.get(adj, "")
                if ch == "":
                    is_valid = False
                else:
                    flooded.add(adj)
                    valid.add(adj)
                    stack.append(adj)
        return is_valid, valid, flooded

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

    def draw(self):
        loop = self.explore().keys()
        inner = self.find_inner()
        rows = []
        for y in range(*self.y_range):
            row = []
            for x in range(*self.x_range):
                coord = (x, y)
                if coord in inner:
                    row.append('*')
                elif coord in loop:
                    # row.append('o')
                    row.append(self.map[coord])
                else:
                    row.append('.')
            rows.append(''.join(row))
        return '\n'.join(rows)




maze = Maze(data)
dist = maze.explore()
x = max(dist.items(), key=lambda x: x[1])[1]
print(x)

inner = maze.find_inner()
print(len(inner))
