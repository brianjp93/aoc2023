from pathlib import Path
from dataclasses import dataclass
from itertools import combinations
from typing import Self

data = (Path(__file__).parent.parent / "data" / "day24.txt").read_text()
# data = """
# 19, 13, 30 @ -2,  1, -2
# 18, 19, 22 @ -1, -1, -2
# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1
# 20, 19, 15 @  1, -5, -3
# """.strip()

# data = """
# 19, 13, 30 @ -2, 1, -2
# 18, 19, 22 @ -1, -1, -2
# """.strip()

@dataclass
class Stone:
    x: int
    y: int
    z: int
    v: tuple[int, int, int]

    def calc_pos(self, t: int | float):
        x = self.x + self.v[0] * t
        y = self.y + self.v[1] * t
        z = self.z + self.v[2] * t
        return x, y, z

    def find_collision_xy(self, other: Self):
        p1 = (self.v[0] * (other.y - self.y))
        p2 = (self.v[1] * (self.x - other.x))
        den = (other.v[0] * self.v[1]) - (other.v[1] * self.v[0])
        if den == 0:
            return False
        t2 =  (p1 + p2) / den
        if t2 < 0:
            return False
        x, y, _ = other.calc_pos(t2)
        t1 = (x - self.x) / self.v[0]
        if t1 < 0:
            return False
        return x, y


def parse(data):
    stones: list[Stone] = []
    for line in data.splitlines():
        a, b = line.split('@')
        x, y, z = map(int, a.split(', '))
        vx, vy, vz = map(int, b.split(', '))
        print(x, y, z, vx, vy, vz)
        stones.append(Stone(x, y, z, (vx, vy, vz)))
    return stones


def part1():
    count = 0
    stones = parse(data)
    print(stones)
    # zone_min = 7
    # zone_max = 27
    zone_min = 200000000000000
    zone_max = 400000000000000
    for a, b in combinations(stones, 2):
        # print(f"Looking at {a=} and {b=}")
        if out := a.find_collision_xy(b):
            x, y = out
            if zone_min <= x <= zone_max and zone_min <= y <= zone_max:
                print(f"Found collision: {(x, y)=}")
                count += 1
    return count


if __name__ == "__main__":
    print(f"{part1()=}")
