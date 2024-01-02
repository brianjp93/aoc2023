from copy import deepcopy
from pathlib import Path
from typing import Self
from dataclasses import dataclass, field


data = (Path(__file__).parent.parent / "data" / "day22.txt").read_text()

@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other: Self):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Self):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)


@dataclass
class Brick:
    units: set[Point]

    def __hash__(self) -> int:
        return hash(id(self))

    @classmethod
    def parse(cls, data):
        a, b = data.split("~")
        x0, y0, z0 = map(int, a.split(","))
        x1, y1, z1 = map(int, b.split(","))
        units = set()
        if x0 != x1:
            x0, x1 = min(x0, x1), max(x0, x1)
            for i in range(x0, x1 + 1):
                units.add(Point(i, y0, z0))
        elif y1 != y0:
            y0, y1 = min(y0, y1), max(y0, y1)
            for i in range(y0, y1 + 1):
                units.add(Point(x0, i, z0))
        elif z0 != z1:
            z0, z1 = min(z0, z1), max(z0, z1)
            for i in range(z0, z1 + 1):
                units.add(Point(x0, y0, i))
        else:
            units.add(Point(x0, y0, z1))
        return cls(units=units)

    def move_down(self):
        units = set()
        for point in self.units:
            units.add(point + Point(0, 0, -1))
        self.units = units

    def move_up(self):
        units = set()
        for point in self.units:
            units.add(point + Point(0, 0, 1))
        self.units = units

@dataclass
class Tower:
    bricks: list[Brick]
    points: set[Point] = field(default_factory=set)
    brick_map: dict[Point, Brick] = field(default_factory=dict)

    def __hash__(self):
        return hash(id(self))

    def __post_init__(self):
        for brick in self.bricks:
            self.points |= brick.units
            for point in brick.units:
                self.brick_map[point] = brick

    def remove(self, brick: Brick):
        self.points -= brick.units
        for point in brick.units:
            del self.brick_map[point]

    def add(self, brick: Brick):
        self.points |= brick.units
        for point in brick.units:
            self.brick_map[point] = brick

    def fall(self):
        self.bricks.sort(key=lambda x: min(y.z for y in x.units))
        count = 0
        for brick in self.bricks:
            self.remove(brick)
            overlap = set()
            down_move = -1
            while not overlap and min(x.z for x in brick.units) > 0:
                brick.move_down()
                overlap = self.points & brick.units
                down_move += 1
            if down_move >= 1:
                count += 1
            brick.move_up()
            self.add(brick)
        return count

    def supporting(self, brick: Brick):
        bricks: set[Brick] = set()
        for point in brick.units:
            above = point + Point(0, 0, 1)
            if other := self.brick_map.get(above, None):
                if other is not brick:
                    bricks.add(other)
        return bricks

    def supported_by(self, brick: Brick):
        bricks: set[Brick] = set()
        for point in brick.units:
            above = point + Point(0, 0, -1)
            if other := self.brick_map.get(above, None):
                if other is not brick:
                    bricks.add(other)
        return bricks

    def disintegratable(self):
        bricks: list[Brick] = []
        for brick in self.bricks:
            supporting = self.supporting(brick)
            if not supporting:
                bricks.append(brick)
            else:
                is_safe = True
                for supported in supporting:
                    if len(self.supported_by(supported)) <= 1:
                        is_safe = False
                        break
                if is_safe:
                    bricks.append(brick)
        return bricks


def parse(data):
    return Tower(bricks=[Brick.parse(line) for line in data.splitlines()])


def part1(tower: Tower):
    breakable = tower.disintegratable()
    return len(breakable)


def part2():
    big = 0
    tower = parse(data)
    tower.fall()
    for i in range(len(tower.bricks)):
        # t = parse(data)
        t = deepcopy(tower)
        t.fall()
        brick = t.bricks[i]
        t.remove(brick)
        del t.bricks[i]
        big += t.fall()
        print(f"Looking at brick {i=}, {big=}")
    return big

if __name__ == '__main__':
    tower = parse(data)
    tower.fall()
    print(f"{part1(tower)=}")
    print(f"{part2()=}")
