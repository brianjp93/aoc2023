from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, TypeAlias
from math import lcm

data = (Path(__file__).parent.parent / "data" / "day20.txt").read_text()


Power: TypeAlias = Literal["high", "low"]
Module: TypeAlias = "Broadcaster | FlipFlop | Conjunction"


@dataclass
class Pulse:
    from_: str
    to: str
    power: Power


@dataclass
class FlipFlop:
    name: str
    to: list[str]
    on: bool = False

    def send(self, pulse: Pulse):
        if pulse.power == "high":
            return
        elif pulse.power == "low":
            self.on = not self.on
        npower = "high" if self.on else "low"
        for item in self.to:
            yield Pulse(from_=self.name, to=item, power=npower)


@dataclass
class Broadcaster:
    name: str
    to: list[str]

    def send(self, pulse: Pulse):
        for item in self.to:
            yield Pulse(from_=self.name, to=item, power=pulse.power)


@dataclass
class Conjunction:
    name: str
    to: list[str]
    memory: dict[str, Literal["high", "low"]] = field(default_factory=dict)

    @property
    def power(self):
        return 'low' if all(x == "high" for x in self.memory.values()) else 'high'

    def send(self, pulse: Pulse):
        self.memory[pulse.from_] = pulse.power
        power = self.power
        for item in self.to:
            yield Pulse(from_=self.name, to=item, power=power)


@dataclass
class System:
    modules: dict[str, Module]
    pulse_buffer: list[Pulse] = field(default_factory=list)
    low_count = 0
    high_count = 0
    sent: dict = field(default_factory=dict)
    count = 0

    def push(self):
        self.count += 1
        self.pulse_buffer.append(Pulse(from_="button", to="broadcaster", power="low"))
        while self.pulse_buffer:
            pulse = self.pulse_buffer.pop(0)
            if pulse.power == "low":
                self.low_count += 1
            else:
                self.high_count += 1
            module = self.modules.get(pulse.to, None)
            if not module:
                continue
            for npulse in module.send(pulse):
                if npulse.from_ not in self.sent:
                    self.sent[npulse.from_] = [npulse.power, []]
                if npulse.power == 'high' and self.sent[npulse.from_][0] == 'low':
                    self.sent[npulse.from_][1].append(self.count)
                self.pulse_buffer.append(npulse)


def parse(data):
    modules: dict[str, Module] = {}
    for line in data.splitlines():
        a, b = line.split(" -> ")
        to = [x.strip() for x in b.split(",")]
        if a == "broadcaster":
            modules["broadcaster"] = Broadcaster("broadcaster", to=to)
        elif a[0] == "%":
            modules[a[1:]] = FlipFlop(a[1:], to=to)
        elif a[0] == "&":
            modules[a[1:]] = Conjunction(a[1:], to=to)
        else:
            raise Exception("???")
    # initialize memory to low
    for module in modules.values():
        for other_str in module.to:
            other = modules.get(other_str, None)
            match other:
                case Conjunction():
                    other.memory[module.name] = "low"
                case _:
                    pass
    return System(modules)


def part1():
    system = parse(data)
    for _ in range(1000):
        system.push()
    return system.low_count * system.high_count


def part2():
    system = parse(data)
    watching = ['ph', 'vn', 'kt', 'hn']

    while True:
        system.push()
        found_all = True
        for item in watching:
            _, b = system.sent.get(item, [None, []])
            if len(b) < 2:
                found_all = False
        if found_all:
            break
    periods = []
    for item in watching:
        diffs = system.sent[item][1]
        periods.append(diffs[1] - diffs[0])
    return lcm(*periods)


if __name__ == "__main__":
    print(f"{part1()=}")
    print(f"{part2()=}")
