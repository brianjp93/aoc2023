import math
data = """Time:        40     81     77     72
Distance:   219   1012   1365   1089"""

def find_wins(best_time: int, distance: int):
    return sum(is_win(best_time, distance, i) for i in range(best_time))

def is_win(best_time: int, distance: int, wind_up: int):
    return (best_time - wind_up) * wind_up > distance

def parse(data):
    lines = data.splitlines()
    times = [int(x) for x in lines[0].split(":")[-1].split()]
    distances = [int(x) for x in lines[1].split(":")[-1].split()]
    return times, distances

if __name__ == '__main__':
    times, distances = parse(data)
    print(math.prod(find_wins(time, dist) for time, dist in zip(times, distances)))

    time, dist = int(''.join(map(str, times))), int(''.join(map(str, distances)))
    x = find_wins(time, dist)
    print(x)
