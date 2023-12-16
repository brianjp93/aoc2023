from pathlib import Path
from dataclasses import dataclass, field

data = (Path(__file__).parent.parent / "data" / "day15.txt").read_text()


@dataclass
class HashMap:
    m: list[list[tuple[str, int]]] = field(default_factory=lambda: [[] for _ in range(257)])

    def __setitem__(self, label: str, value: int):
        idx = do_hash(label)
        if lst := [(i, x[0]) for i, x in enumerate(self.m[idx]) if x[0] == label]:
            box_idx, label = lst[0]
            self.m[idx][box_idx] = (label, value)
        else:
            self.m[idx].append((label, value))

    def __delitem__(self, label: str):
        idx = do_hash(label)
        if lst := [(i, x[0]) for i, x in enumerate(self.m[idx]) if x[0] == label]:
            box_idx, label = lst[0]
            del self.m[idx][box_idx]


def do_hash(item: str):
    val = 0
    for ch in item:
        val += ord(ch)
        val *= 17
    return val % 256


if __name__ == "__main__":
    data = data.strip().split(",")
    print(sum(do_hash(line) for line in data))

    hm = HashMap()
    for line in data:
        if '=' in line:
            label, focal = line.split('=')
            hm[label] = int(focal)
        elif '-' in line:
            del hm[line.rstrip('-')]

    focusing_power = sum(
        sum((i+1) * focal * j for j, (_, focal) in enumerate(box, 1))
        for i, box in enumerate(hm.m)
    )
    print(focusing_power)
