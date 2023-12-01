from pathlib import Path
import re

data = (Path(__file__).parent.parent / "data" / "day01.txt").read_text()

pat1 = re.compile(r"\d")
pat2 = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))")

DIGITS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

def get_sum(data: str, pattern: re.Pattern[str]):
    total = 0
    for line in data.splitlines():
        matches = pattern.findall(line)
        total += int(''.join(map(lambda x: DIGITS.get(x, x), (matches[0], matches[-1]))))
    return total

print(get_sum(data, pat1))
print(get_sum(data, pat2))
