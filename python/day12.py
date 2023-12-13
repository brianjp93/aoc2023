from pathlib import Path
from functools import lru_cache


data = (Path(__file__).parent.parent / "data" / "day12.txt").read_text()


def unfold(row: str, pattern: tuple[int, ...]):
    return "?".join(row for _ in range(5)), tuple(list(pattern) * 5)


def parse(data):
    output: list[tuple[ str, tuple[int, ...] ]] = []
    for line in data.splitlines():
        a, b = line.split()
        nums = tuple(map(int, b.split(',')))
        output.append((a, nums))
    return output


@lru_cache
def recurse(row: str, pattern: tuple[int, ...]):
    if not pattern:
        if '#' not in row:
            return 1
        return 0
    elif not row:
        return 0

    count = pattern[0]
    if count <= len(row.split('.')[0]):
        count1 = recurse(row[count + 1:], pattern[1:]) if row[count] != '#' else 0
        count2 = recurse(row[1:], pattern[:]) if row[0] == '?' else 0
        return count1 + count2
    elif row[0] != "#":
        return recurse(row[1:], pattern[:])
    return 0


def possible_count(rows: list[tuple[str, tuple[int, ...]]], is_unfold=False):
    for row, pattern in rows:
        if is_unfold:
            row, pattern = unfold(row, pattern)
        yield recurse(row + ".", pattern)


if __name__ == '__main__':
    output = parse(data)

    p1 = sum(possible_count(output))
    print(f"{p1=}")
    p2 = sum(possible_count(output, is_unfold=True))
    print(f"{p2=}")
