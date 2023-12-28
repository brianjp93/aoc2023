from pathlib import Path
from typing import TypeAlias
from queue import SimpleQueue as Queue, Empty
from dataclasses import dataclass
from math import inf


data = (Path(__file__).parent.parent / "data" / "day21.txt").read_text()


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y)


DIRS = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]


def get_adj(point: Point):
    for d in DIRS:
        yield point + d


Map: TypeAlias = dict[Point, str]

@dataclass
class Farm:
    m: Map
    start: Point

    def __post_init__(self):
        self.max_x = max(x.x for x in self.m.keys())
        self.max_y = max(x.y for x in self.m.keys())

    def __getitem__(self, point: Point):
        # get item in an infinitely repeating map
        x = point.x % (self.max_x + 1)
        y = point.y % (self.max_y + 1)
        point = Point(x, y)
        return self.m[point]

    @classmethod
    def parse(cls, data):
        m: Map = {}
        start = Point(0, 0)
        for y, row in enumerate(data.splitlines()):
            for x, ch in enumerate(row):
                if ch == 'S':
                    start = Point(x, y)
                    m[Point(x, y)] = '.'
                else:
                    m[Point(x, y)] = ch
        return cls(m=m, start=start)

    def find_reachable(self, steps=64):
        queue: Queue[tuple[int, Point]] = Queue()
        queue.put((0, self.start), block=False)
        min_dist: dict[Point, int] = {}
        while True:
            try:
                dist, point = queue.get(block=False)
            except Empty:
                break
            if dist > steps:
                continue

            if min_dist.get(point, inf) <= dist:
                continue
            min_dist[point] = dist

            for adj in get_adj(point):
                if self.m.get(adj, '#') == '.':
                    queue.put((dist + 1, adj), block=False)
        return sum(1 for x in min_dist.values() if (steps - x) % 2 == 0)


    def find_reachable2(self, steps=64):
        queue: Queue[tuple[int, Point]] = Queue()
        queue.put((0, self.start), block=False)
        min_dist: dict[Point, int] = {}
        while True:
            try:
                dist, point = queue.get(block=False)
            except Empty:
                break
            if dist > steps:
                continue

            if min_dist.get(point, inf) <= dist:
                continue
            min_dist[point] = dist

            for adj in get_adj(point):
                if self[adj] == '.':
                    queue.put((dist + 1, adj), block=False)
        return sum(1 for x in min_dist.values() if (steps - x) % 2 == 0)


def part1():
    farm = Farm.parse(data)
    reachable = farm.find_reachable(64)
    return reachable


def part2():
    farm = Farm.parse(data)
    step = farm.max_x + 1
    total_steps = 26501365
    offset_start = total_steps % step
    i = offset_start
    reachable = []
    for _ in range(3):
        reachable.append(farm.find_reachable2(i))
        i += step


    diff1 = [b - a for a, b in zip(reachable, reachable[1:])]
    diff2 = diff1[1] - diff1[0]
    start = reachable[1]
    addition = diff1[0]
    i = step + offset_start
    while i != total_steps:
        addition += diff2
        start += addition
        i += step
    return start


print(f"{part1()=}")
print(f"{part2()=}")
