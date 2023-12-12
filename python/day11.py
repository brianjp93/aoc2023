from pathlib import Path
from dataclasses import dataclass
from typing import TypeAlias

data = (Path(__file__).parent.parent / "data" / "day11.txt").read_text()

Coord: TypeAlias = tuple[int, int]


@dataclass
class Universe:
    map: list[list[str]]

    def find_empty(self):
        empty_rows = []
        for y, row in enumerate(self.map):
            if all(ch == "." for ch in row):
                empty_rows.append(y)

        empty_cols = []
        for x in range(len(self.map[0])):
            if all(self.map[y][x] == "." for y in range(len(self.map))):
                empty_cols.append(x)
        return empty_rows, empty_cols

    def stars(self):
        stars = []
        for y, row in enumerate(self.map):
            for x, ch in enumerate(row):
                if ch == "#":
                    stars.append((x, y))
        return stars

    def find_distances(self):
        dist = 0
        stars = self.stars()
        for i, star in enumerate(stars[:-1]):
            for other in stars[i+1:]:
                dist += abs(star[0] - other[0]) + abs(star[1] - other[1])
        return dist

    def calculate_expansions(self):
        stars = self.stars()
        empty_rows, empty_cols = self.find_empty()
        multiple = 0
        for i, star in enumerate(stars[:-1]):
            for other in stars[i+1:]:
                for row in empty_rows:
                    if min(star[1], other[1]) < row < max(star[1], other[1]):
                        multiple += 1
                for col in empty_cols:
                    if min(star[0], other[0]) < col < max(star[0], other[0]):
                        multiple += 1
        return multiple


def parse(data):
    rows = []
    for line in data.splitlines():
        rows.append([x for x in line])
    return Universe(map=rows)


if __name__ == '__main__':
    x = parse(data)
    initial = x.find_distances()
    multiple = x.calculate_expansions()

    p1 = initial + multiple
    print(f"{p1=}")
    p2 = initial + (multiple * 999999)
    print(f"{p2=}")
