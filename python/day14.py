from pathlib import Path
from typing import TypeAlias
from itertools import count


data = (Path(__file__).parent.parent / "data" / "day14.txt").read_text()

ROUND = "O"
CUBE = "#"
OPEN = "."


Map: TypeAlias = list[list[str]]
TupleMap: TypeAlias = tuple[tuple[str, ...], ...]


def parse(data):
    rows: Map = []
    for line in data.splitlines():
        rows.append([x for x in line])
    return rows


def slide_north(m: Map) -> Map:
    for y, row in enumerate(m):
        for x, ch in enumerate(row):
            if ch == ROUND:
                cy = y
                while cy - 1 >= 0 and m[cy - 1][x] != CUBE:
                    m[cy][x], m[cy - 1][x] = m[cy - 1][x], m[cy][x]
                    cy -= 1
    return m


def slide_south(m: Map) -> Map:
    length = len(m)
    for y in range(length - 1, -1, -1):
        row = m[y]
        for x, ch in enumerate(row):
            if ch == ROUND:
                cy = y
                while cy + 1 < length and m[cy + 1][x] != CUBE:
                    m[cy][x], m[cy + 1][x] = m[cy + 1][x], m[cy][x]
                    cy += 1
    return m


def slide_west(m: Map) -> Map:
    for y, row in enumerate(m):
        for x, ch in enumerate(row):
            if ch == ROUND:
                cx = x
                while cx - 1 >= 0 and m[y][cx - 1] != CUBE:
                    m[y][cx], m[y][cx - 1] = m[y][cx - 1], m[y][cx]
                    cx -= 1
    return m


def slide_east(m: Map) -> Map:
    length = len(m[0])
    for y, row in enumerate(m):
        for x in range(length - 1, -1, -1):
            ch = row[x]
            if ch == ROUND:
                cx = x
                while cx + 1 < length and m[y][cx + 1] != CUBE:
                    m[y][cx], m[y][cx + 1] = m[y][cx + 1], m[y][cx]
                    cx += 1
    return m

def cycle(m: Map):
    slide_north(m)
    slide_west(m)
    slide_south(m)
    slide_east(m)


def hashable(m: Map):
    return tuple(tuple(x for x in row) for row in m)

def unhashable(m: TupleMap):
    return list(list(x for x in row) for row in m)


def find_cycles(m: Map):
    found: dict[tuple[tuple[str, ...], ...], list[int]] = {}
    hashm = hashable(m)
    found[hashm] = [0]
    for i in count():
        cycle(m)
        hashm = hashable(m)
        if hashm in found:
            found[hashm].append(i + 1)
            return hashm, found
        else:
            found[hashm] = [i + 1]
    raise Exception("uh oh")


def calculate_load(m: Map | TupleMap):
    height = len(m)
    total = 0
    for y, row in enumerate(m):
        for ch in row:
            if ch == ROUND:
                total += height - y
    return total


def get_index(idx: int, m: Map):
    hashm, found = find_cycles(m)
    end_map = unhashable(hashm)
    a, b = found[hashm]
    cycle_length = b - a
    after_start = idx - b
    mod = after_start % cycle_length

    for _ in range(mod):
        cycle(end_map)
    return end_map


if __name__ == '__main__':
    m = parse(data)
    slide_north(m)
    load = calculate_load(m)
    print(load)

    m = parse(data)
    m = get_index(1000000000, m)
    print(calculate_load(m))
