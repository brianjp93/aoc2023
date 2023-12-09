from pathlib import Path

data = (Path(__file__).parent.parent / "data" / "day09.txt").read_text()

def predict_next(values: list[int]):
    diff = [b - a for a, b in zip(values, values[1:])]
    val = 0 if all(x == 0 for x in diff) else predict_next(diff)[-1]
    return values + [values[-1] + val]

items = [list(map(int, line.split())) for line in data.splitlines()]
print(sum(predict_next(item)[-1] for item in items))
print(sum(predict_next(item[::-1])[-1] for item in items))
