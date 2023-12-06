from pathlib import Path
from dataclasses import dataclass, field

data = (Path(__file__).parent.parent / "data" / "day05.txt").read_text()
# data = """seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# 52 50 48

# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15

# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4

# water-to-light map:
# 88 18 7
# 18 25 70

# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13

# temperature-to-humidity map:
# 0 69 1
# 1 0 69

# humidity-to-location map:
# 60 56 37
# 56 93 4"""


@dataclass
class MapItem:
    destination: int
    source: int
    range: int


@dataclass
class Mapping:
    type: str
    items: list[MapItem] = field(default_factory=list)


@dataclass
class Almanac:
    mappings: dict[str, Mapping]
    seeds: list[int]

    def convert(self, n: int, start='seed', to='soil'):
        key = f'{start}-to-{to}'
        mapping = self.mappings[key]
        for item in mapping.items:
            if n in range(item.source, item.source + item.range + 1):
                offset = n - item.source
                mapped_num = item.destination + offset
                return mapped_num
        return n

    def convert_to(self, n: int, final='location'):
        start = 'seed'
        to = 'soil'
        while True:
            n = self.convert(n, start, to)
            if to == final:
                return n
            for mapping in self.mappings.values():
                if mapping.type.startswith(to):
                    start, to = mapping.type.split('-to-')
                    break

    def convert_backward(self, n: int, start, to):
        key = f'{start}-to-{to}'
        mapping = self.mappings[key]
        for item in mapping.items:
            if item.destination <= n < item.destination + item.range:
                offset = n - item.destination
                mapped_num = item.source + offset
                return mapped_num
        return n

    def convert_backward_full(self, n: int, final='seed'):
        start = 'humidity'
        to = 'location'
        while True:
            n = self.convert_backward(n, start, to)
            if start == final:
                return n
            for mapping in self.mappings.values():
                if mapping.type.endswith(start):
                    start, to = mapping.type.split('-to-')
                    break

    def is_valid_seed(self, seed: int):
        for i in range(0, len(self.seeds), 2):
            start, length = self.seeds[i:i+2]
            if start <= seed < start + length:
                return True
        return False


def parse(data):
    seeds = []
    mappings = {}
    for part in data.split('\n\n'):
        if part.startswith('seeds:'):
            seeds = list(map(int, part.lstrip('seeds: ').split()))
        else:
            lines = iter(part.splitlines())
            l1 = next(lines)
            _type = l1.split()[0]
            mapping = Mapping(type=_type)
            for line in lines:
                destination, source, _range = list(map(int, line.split()))
                mapping.items.append(MapItem(destination=destination, source=source, range=_range))
            mappings[mapping.type] = mapping
    return Almanac(mappings=mappings, seeds=seeds)


def convert_ranges(almanac: Almanac):
    for i in range(0, len(almanac.seeds), 2):
        start, _range = almanac.seeds[i:i+2]
        for n in range(start, start + _range + 1):
            yield almanac.convert_to(n)


if __name__ == '__main__':
    almanac = parse(data)
    print(min(almanac.convert_to(seed) for seed in almanac.seeds))

    is_valid = False
    location = 0
    while not is_valid:
        # if location % 10000 == 0:
        #     print(f'checking {location=}')
        #     pass
        seed = almanac.convert_backward_full(location)
        if almanac.is_valid_seed(seed):
            print(f'location {location=}')
            break
        location += 1
