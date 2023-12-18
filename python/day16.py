from pathlib import Path
from dataclasses import dataclass

data = (Path(__file__).parent.parent / "data" / "day16.txt").read_text()


UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)
UPRIGHT = "/"
DOWNRIGHT = "\\"
PIPE = "|"
DASH = "-"

REDIRECTION = {
    (RIGHT, UPRIGHT): [UP],
    (RIGHT, DOWNRIGHT): [DOWN],
    (RIGHT, PIPE): [UP, DOWN],

    (DOWN, UPRIGHT): [LEFT],
    (DOWN, DOWNRIGHT): [RIGHT],
    (DOWN, DASH): [LEFT, RIGHT],

    (LEFT, UPRIGHT): [DOWN],
    (LEFT, DOWNRIGHT): [UP],
    (LEFT, PIPE): [DOWN, UP],

    (UP, UPRIGHT): [RIGHT],
    (UP, DOWNRIGHT): [LEFT],
    (UP, DASH): [LEFT, RIGHT],
}


@dataclass
class Map:
    m: list[str]

    @classmethod
    def parse(cls, data):
        return cls(m=data.splitlines())

    def get(self, x: int, y: int, default=None):
        if x < 0 or y < 0:
            return default
        try:
            return self.m[y][x]
        except IndexError:
            return default

    def draw_beam(self, start=((0, 0), RIGHT)):
        beam = set()
        seen = set()
        stack = [start]
        while stack:
            coord, vector = stack.pop()
            ch = self.get(*coord)
            if not ch:
                continue
            seen.add((coord, vector))
            beam.add(coord)
            key = (vector, ch)
            for nvector in REDIRECTION.get(key, [vector]):
                ncoord = coord[0] + nvector[0], coord[1] + nvector[1]
                if (ncoord, nvector) not in seen:
                    stack.append((ncoord, nvector))
        return beam

    def highest(self):
        max_x = len(self.m[0]) - 1
        max_y = len(self.m) - 1
        high = 0
        for x in range(max_x + 1):
            high = max(len(self.draw_beam(((x, 0), DOWN))), high)
            high = max(len(self.draw_beam(((x, max_y), UP))), high)
        for y in range(max_y + 1):
            high = max(len(self.draw_beam(((0, y), RIGHT))), high)
            high = max(len(self.draw_beam(((max_x, y), LEFT))), high)
        return high


if __name__ == '__main__':
    m = Map.parse(data)
    beam = m.draw_beam()
    print(len(beam))
    print(m.highest())
