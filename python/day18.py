from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypeAlias

data = (Path(__file__).parent.parent / "data" / "day18.txt").read_text()


# data = """R 6 (#70c710)
# D 5 (#0dc571)
# L 2 (#5713f0)
# D 2 (#d2c081)
# R 2 (#59c680)
# D 2 (#411b91)
# L 5 (#8ceee2)
# U 2 (#caa173)
# L 1 (#1b58a2)
# U 2 (#caa171)
# R 2 (#7807d2)
# U 3 (#a77fa3)
# L 2 (#015232)
# U 2 (#7a21e3)"""


Coord: TypeAlias = tuple[int, int]
Map: TypeAlias = set[Coord]
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS: dict[str, Coord] = {
    "U": UP,
    "D": DOWN,
    "R": RIGHT,
    "L": LEFT,
}

@dataclass
class Line:
    c1: Coord
    c2: Coord

    orientation: Literal['x', 'y']
    is_wall: bool


def parse(data):
    for line in data.splitlines():
        a, b, _ = line.split()
        yield DIRECTIONS[a], int(b)


def parse2(data):
    for line in data.splitlines():
        *_, c = line.split()
        c = c.lstrip("(#").rstrip(")")
        color_int = int(c[-1])
        d = [RIGHT, DOWN, LEFT, UP][color_int]
        yield d, int(c[:5], 16)


def add(c1: Coord, c2: Coord):
    return (c1[0] + c2[0], c1[1] + c2[1])

def get_lines(data, p2=False):
    start = (0, 0)
    all_data = list(parse2(data) if p2 else parse(data))
    for i, (facing, b) in enumerate(all_data):
        end = add((facing[0] * b, facing[1] * b), start)
        prev_facing = all_data[i - 1][0]
        next_facing = all_data[(i + 1) % len(all_data)][0]
        is_wall = False
        if start[0] == end[0]:
            orientation = 'y'
        else:
            orientation = 'x'
            is_wall = prev_facing == next_facing
        yield Line(start, end, orientation, is_wall)
        start = end


def get_horizontal(lines: list[Line]):
    hz: dict[tuple[Coord, Coord], Line] = {}
    for line in lines:
        if line.orientation == 'x':
            c1 = min(line.c1, line.c2)
            c2 = max(line.c1, line.c2)
            hz[(c1, c2)] = line
    return hz


def find_vertical_lines(lines: tuple[Line, ...], y: int):
    for line in lines:
        if line.c1[1] < line.c2[1]:
            min_y = line.c1[1]
            max_y = line.c2[1]
        else:
            min_y = line.c2[1]
            max_y = line.c1[1]
        if min_y <= y <= max_y:
            yield line

def get_line_area(lines: list[Line]):
    min_y = min(min(line.c1[1], line.c2[1]) for line in lines)
    max_y = max(max(line.c1[1], line.c2[1]) for line in lines)
    hz = get_horizontal(lines)
    lines.sort(key=lambda x: x.c1[0])
    vertical_lines = tuple(line for line in lines if line.orientation == 'y')
    area = 0
    for y in range(min_y, max_y + 1):
        wall_count = 0
        ver_lines = tuple(find_vertical_lines(vertical_lines, y))
        seen = []
        prev_is_flat_wall = False
        for i in range(len(ver_lines) - 1):
            a = ver_lines[i]
            b = ver_lines[i+1]
            start = (a.c1[0], y)
            end = (b.c1[0], y)
            key = (start, end)
            length = end[0] - start[0] + 1
            if start in seen:
                length -= 1
            if line := hz.get(key):
                # print(f"found {key=}")
                # print(f"Adding {length=}")
                area += length
                if line.is_wall:
                    wall_count += 1
                prev_is_flat_wall = True
                seen.append(end)
            else:
                if not prev_is_flat_wall:
                    wall_count += 1
                if wall_count % 2 == 1:
                    area += length
                    # print(f"Adding {length=}")
                    seen.append(end)
                prev_is_flat_wall = False
    return area


lines = list(get_lines(data))
area = get_line_area(lines)
print(area)
lines = list(get_lines(data, p2=True))
area = get_line_area(lines)
print(area)
