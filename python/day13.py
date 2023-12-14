from pathlib import Path
from dataclasses import dataclass
from enum import Enum


data = (Path(__file__).parent.parent / "data" / "day13.txt").read_text()


class Orientation(Enum):
    VERTICAL = 0
    HORIZONTAL = 1


@dataclass
class Map:
    map: list[str]

    def find_reflection(self, smudge=False):
        x = self.find_vertical_reflection(smudge=smudge)
        if x is not False:
            return Orientation.VERTICAL, x
        y = self.find_horizontal_reflection(smudge=smudge)
        if y is not False:
            return Orientation.HORIZONTAL, y
        raise Exception('uh oh')

    def find_vertical_reflection(self, smudge=False):
        xlength = len(self.map[0])
        ylength = len(self.map)
        for x in range(xlength - 1):
            error = 0
            for lx, rx in zip(range(x, -1, -1), range(x + 1, xlength)):
                lcol = tuple(self.map[y][lx] for y in range(ylength))
                rcol = tuple(self.map[y][rx] for y in range(ylength))
                error += sum(a != b for a, b in zip(lcol, rcol))
            if (smudge and error == 1) or (not smudge and error == 0):
                return x
        return False

    def find_horizontal_reflection(self, smudge=False):
        ylength = len(self.map)
        for y in range(ylength - 1):
            error = 0
            for ly, ry in zip(range(y, -1, -1), range(y + 1, ylength)):
                error += sum(a != b for a, b in zip(self.map[ly], self.map[ry]))
            if (smudge and error == 1) or (not smudge and error == 0):
                return y
        return False

    def summary(self, smudge=False):
        ori, idx = self.find_reflection(smudge=smudge)
        return (idx + 1) * 100 if ori == Orientation.HORIZONTAL else idx + 1


def parse(data):
    maps: list[Map] = []
    for m in data.split("\n\n"):
        maps.append(Map(m.splitlines()))
    return maps


if __name__ == '__main__':
    maps = parse(data)
    print(sum(m.summary() for m in maps))
    print(sum(m.summary(smudge=True) for m in maps))
