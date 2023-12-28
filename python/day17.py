from pathlib import Path
from typing import TypeAlias
from queue import Empty, PriorityQueue

Coord: TypeAlias = tuple[int, int]
Map: TypeAlias = dict[Coord, int]

data = (Path(__file__).parent.parent / "data" / "day17.txt").read_text()


DIRECTIONS = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]

REVERSE: dict[Coord, Coord] = {
    (1, 0): (-1, 0),
    (-1, 0): (1, 0),
    (0, 1): (0, -1),
    (0, -1): (0, 1),
}


def parse(data):
    m: dict[Coord, int] = {}
    for y, line in enumerate(data.splitlines()):
        for x, ch in enumerate(line):
            m[(x, y)] = int(ch)
    return m


def get_adj(m: Map, coord: Coord):
    for d in DIRECTIONS:
        ncoord = d[0] + coord[0], d[1] + coord[1]
        n = m.get(ncoord, None)
        if n is not None:
            yield ncoord, n, d


def shortest_path(m: Map, must_turn_min=0, must_turn_max=3):
    seen: dict[tuple[Coord, int, Coord], int] = {}
    stack: PriorityQueue[tuple[int, Coord, int, Coord]] = PriorityQueue()
    stack.put((0, (0, 0), 0, (0, 0)), block=False)
    max_x = max(x[0] for x in m.keys())
    max_y = max(x[1] for x in m.keys())
    end = (max_x, max_y)
    short = float('inf')
    while True:
        try:
            heat_loss, coord, turn, facing = stack.get(block=False)
        except Empty:
            break

        # check cache
        key = (coord, turn, facing)
        if heat_loss >= seen.get(key, float('inf')):
            continue
        seen[key] = heat_loss

        if coord == end:
            if turn >= must_turn_min:
                short = min(short, heat_loss)
            continue

        if heat_loss == 0:
            for adj, nheat, nfacing in get_adj(m, coord):
                stack.put((nheat, adj, 1, nfacing), block=False)
            continue

        if turn < must_turn_min:
            ncoord = facing[0] + coord[0], facing[1] + coord[1]
            nheat = m.get(ncoord, None)
            if nheat is not None:
                stack.put((nheat + heat_loss, ncoord, turn + 1, facing), block=False)
            continue

        if must_turn_min <= turn <= must_turn_max:
            for ncoord, nheat, d in get_adj(m, coord):
                if REVERSE[facing] == d:
                    continue

                if d == facing:
                    nturn = turn + 1
                    if nturn > must_turn_max:
                        continue
                else:
                    nturn = 1
                stack.put((nheat + heat_loss, ncoord, nturn, d), block=False)

    return short


if __name__ == '__main__':
    m = parse(data)
    short = shortest_path(m)
    print(short)
    short = shortest_path(m, must_turn_min=4, must_turn_max=10)
    print(short)
