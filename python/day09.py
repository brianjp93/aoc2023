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
            diff.append(0)
            val = 0
        else:
            val = self.predict_next(diff)[-1]
        values.append(values[-1] + val)
        return values

    def predict_previous(self, values: list[int]):
        diff = [b - a for a, b in zip(values, values[1:])]
        if all(x == 0 for x in diff):
            val = 0
        else:
            val = self.predict_previous(diff)[0]
        values = [values[0] - val] + values
        return values

def parse(data):
    return [History(list(map(int, line.split()))) for line in data.splitlines()]


if __name__ == '__main__':
    items = parse(data)

    print(sum(item.predict_next(item.history)[-1] for item in items))
    print(sum(item.predict_previous(item.history)[0] for item in items))
