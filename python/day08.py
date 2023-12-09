from itertools import count
from pathlib import Path
from dataclasses import dataclass
from math import lcm

data = (Path(__file__).parent.parent / "data" / "day08.txt").read_text()


@dataclass
class Node:
    name: str
    left: str
    right: str
    end: int | None = None


@dataclass
class Wasteland:
    instr: str
    map: dict[str, Node]

    def find(self):
        name = 'AAA'
        for i in count():
            instr = self.instr[i % len(self.instr)]
            node = self.map[name]
            name = node.left if instr == 'L' else node.right
            if name == 'ZZZ':
                return i + 1

    def find_loops(self):
        nodes = [node for node in self.map.values() if node.name[-1] == 'A']
        for node in nodes:
            current = node
            for i in count():
                instr = self.instr[i % len(self.instr)]
                name = current.left if instr == 'L' else current.right
                current = self.map[name]
                if current.name[-1] == 'Z':
                    node.end = i + 1
                    break
        return nodes


def parse(data):
    mapping = {}
    instr, other = data.split('\n\n')
    for line in other.splitlines():
        name, other = line.split('=')
        a, b = other.split(',')
        name = name.strip()
        a = a.strip().lstrip('(')
        b = b.strip().rstrip(')')
        mapping[name] = Node(name=name, left=a, right=b)
    return Wasteland(instr=instr, map=mapping)


if __name__ == '__main__':
    wasteland = parse(data)

    out = wasteland.find()
    print(out)

    nodes = wasteland.find_loops()
    loops = [node.end for node in nodes if node.end]
    out = lcm(*loops)
    print(out)
