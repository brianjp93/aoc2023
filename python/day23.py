from pathlib import Path
from typing import TypeAlias
from dataclasses import dataclass

Coord: TypeAlias = tuple[int, int]

data = (Path(__file__).parent.parent / "data" / "day23.txt").read_text()

#data = """#.#####################
##.......#########...###
########.#########.#.###
####.....#.>.>.###.#.###
####v#####.#v#.###.#.###
####.>...#.#.#.....#...#
####v###.#.#.#########.#
####...#.#.#.......#...#
######.#.#.#######.#.###
##.....#.#.#.......#...#
##.#####.#.#.#########v#
##.#...#...#...###...>.#
##.#.#v#######v###.###v#
##...#.>.#...>.>.#.###.#
######v#.#.###v#.#.###.#
##.....#...#...#.#.#...#
##.#########.###.#.#.###
##...###...#...#...#.###
####.###.#.###v#####v###
##...#...#.#.>.>.#.>.###
##.###.###.#.###.#.#v###
##.....###...###...#...#
######################.#"""


DIRS = {
    '^': (0, -1),
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
}

def get_adj(coord: Coord):
    for adj in DIRS.values():
        yield coord[0] + adj[0], coord[1] + adj[1]

@dataclass
class Maze:
    m: list[str]

    @classmethod
    def parse(cls, data):
        return cls(m=data.splitlines())

    def __getitem__(self, coord: Coord, default="#"):
        if coord[0] < 0 or coord[1] < 0:
            return default
        try:
            return self.m[coord[1]][coord[0]]
        except IndexError:
            return default

    def traverse(self, slippery=True):
        big = 0
        queue: list[tuple[Coord, int, set[Coord]]] = []
        queue.append(((1, 0), 0, set()))
        goal = (len(self.m[0]) - 2, len(self.m) - 1)
        i = 0
        while queue:
            i += 1
            if i % 10000 == 0:
                print(f"Looking at item {i=}, {len(queue)=}")
            coord, dist, seen = queue.pop()
            if coord == goal:
                if dist > big:
                    big = dist
                print(f"Found a solution at {dist=}, {big=}")
                continue

            val = self[coord]
            seen.add(coord)
            if slippery and val in DIRS.keys():
                vec = DIRS[val]
                valid_dirs = [(coord[0] + vec[0], coord[1] + vec[1])]
            else:
                valid_dirs = get_adj(coord)
            for ncoord in valid_dirs:
                if self[ncoord] != '#' and ncoord not in seen:
                    queue.append((ncoord, dist + 1, seen.copy()))
        return big


def part1():
    maze = Maze.parse(data)
    big = maze.traverse()
    return big


def part2():
    maze = Maze.parse(data)
    big = maze.traverse(slippery=False)
    return big


if __name__ == '__main__':
    # print(f"{part1()=}")  # 1.35s
    print(f"{part2()=}")
