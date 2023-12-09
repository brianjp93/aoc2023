from pathlib import Path
from dataclasses import dataclass

data = (Path(__file__).parent.parent / "data" / "day09.txt").read_text()


@dataclass
class History:
    history: list[int]

    def predict_next(self, values: list[int]):
        values = values.copy()
        diff = [b - a for a, b in zip(values, values[1:])]
        if all(x == 0 for x in diff):
            diff.append(diff[-1])
        else:
            diff.append(self.predict_next(diff)[-1])
        values.append(values[-1] + diff[-1])
        return values

    def predict_previous(self, values: list[int]):
        values = values.copy()
        diff = [b - a for a, b in zip(values, values[1:])]
        if all(x == 0 for x in diff):
            diff.append(0)
        else:
            diff.append(self.predict_next(diff)[-1])
            diff = [self.predict_previous(diff)[0]] + diff
        values.append(values[-1] + diff[-1])
        values = [values[0] - diff[0]] + values
        return values

def parse(data):
    x: list[History] = []
    for line in data.splitlines():
        line = list(map(int, line.split()))
        x.append(
            History(history=line)
        )
    return x


if __name__ == '__main__':
    items = parse(data)

    total = 0
    for item in items:
        values = item.predict_next(item.history)
        total += values[-1]
    print(total)


    total = 0
    for item in items:
        values = item.predict_previous(item.history)
        total += values[0]
    print(total)
