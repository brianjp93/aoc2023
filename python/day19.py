from dataclasses import dataclass
from pathlib import Path
import re
from typing import Literal, Self, TypedDict
from copy import deepcopy
from math import prod

data = (Path(__file__).parent.parent / "data" / "day19.txt").read_text()


class RangeSet:
    def __init__(
        self,
        ranges: list[tuple[int, int]] | None = None,
        start: int | None = None,
        end: int | None = None,
    ):
        if ranges:
            self.ranges = ranges
        else:
            assert isinstance(start, int)
            assert isinstance(end, int)
            self.ranges = [(start, end)]

    def __contains__(self, val: int):
        for r in self.ranges:
            if r[0] <= val <= r[1]:
                return True
        return False

    def __str__(self):
        return f"RangeSet(ranges={self.ranges})"

    def __len__(self):
        return sum(b - a + 1 for a, b in self.ranges)

    def __sub__(self, other: Self):
        new_ranges = []
        for r1 in self.ranges:
            for r2 in other.ranges:
                if r2[0] <= r1[0]:
                    start = r2[1] + 1
                    end = r1[1]
                    if start <= end:
                        new_ranges.append((start, end))
                elif r2[0] <= r1[1]:
                    start = r1[0]
                    end = r2[0] - 1
                    if start <= end:
                        new_ranges.append((start, end))
                    start = r2[1] + 1
                    end = r1[1]
                    if start <= end:
                        new_ranges.append((start, end))
        return self.__class__(ranges=new_ranges)


class Part(TypedDict):
    x: int
    m: int
    a: int
    s: int


@dataclass
class Condition:
    name: str
    comparison: Literal[">", "<"]
    value: int
    action: str


@dataclass
class Workflow:
    name: str
    default: str
    conditions: list[Condition]

    @classmethod
    def parse(cls, instr: str):
        name, b = instr.split("{")
        b = b.rstrip("}")
        b = b.split(",")
        cmps = []
        for part in b[:-1]:
            if "<" in part:
                id_, last = part.split("<")
                comparison = "<"
            else:
                id_, last = part.split(">")
                comparison = ">"
            value, action = last.split(":")
            cmps.append(Condition(id_, comparison, int(value), action=action))
        return cls(name=name, default=b[-1], conditions=cmps)


def parse(data):
    top, bot = data.split("\n\n")
    wfls: dict[str, Workflow] = {}
    parts: list[Part] = []
    for line in top.splitlines():
        workflow = Workflow.parse(line)
        wfls[workflow.name] = workflow
    for p in bot.splitlines():
        x, m, a, s = map(int, re.findall(r"=(\d+)", p))
        parts.append({"x": x, "m": m, "a": a, "s": s})
    return wfls, parts


def get_valid(flows: dict[str, Workflow]):
    ratings: dict[str, RangeSet] = {
        "x": RangeSet(start=1, end=4000),
        "m": RangeSet(start=1, end=4000),
        "a": RangeSet(start=1, end=4000),
        "s": RangeSet(start=1, end=4000),
    }
    stack = [(ratings, flows["in"])]
    valid_ratings: list[dict[str, RangeSet]] = []
    while stack:
        ratings, flow = stack.pop()
        for cond in flow.conditions:
            rating = ratings[cond.name]
            if cond.comparison == "<":
                success = rating - RangeSet(start=cond.value, end=4000)
                failure = rating - RangeSet(start=1, end=cond.value - 1)
            else:
                success = rating - RangeSet(start=1, end=cond.value)
                failure = rating - RangeSet(start=cond.value + 1, end=4000)
            if cond.action == "A":
                nratings = deepcopy(ratings)
                nratings[cond.name] = success
                valid_ratings.append(nratings)
            elif cond.action == "R":
                pass
            else:
                nflow = flows[cond.action]
                nratings = deepcopy(ratings)
                nratings[cond.name] = success
                stack.append((nratings, nflow))
            ratings[cond.name] = failure
        if flow.default == "A":
            valid_ratings.append(ratings)
        elif flow.default == "R":
            pass
        else:
            nflow = flows[flow.default]
            nratings = deepcopy(ratings)
            stack.append((nratings, nflow))
    return valid_ratings


def part1(valid, parts):
    total = 0
    for part in parts:
        for rating in valid:
            if all(
                (
                    part["x"] in rating["x"],
                    part["m"] in rating["m"],
                    part["a"] in rating["a"],
                    part["s"] in rating["s"],
                )
            ):
                total += sum(part.values())
                break
    return total


def part2(valid):
    return sum(prod(len(x) for x in rating.values()) for rating in valid)


if __name__ == "__main__":
    flows, parts = parse(data)
    valid = get_valid(flows)
    print(f"{part1(valid, parts)=}")
    print(f"{part2(valid)=}")
