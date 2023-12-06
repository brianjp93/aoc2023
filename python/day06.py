data = """Time:        40     81     77     72
Distance:   219   1012   1365   1089"""


def find_wins(best_time: int, distance: int):
    total = 0
    for i in range(best_time):
        if is_win(best_time, distance, i):
            total += 1
    return total


def is_win(best_time: int, distance: int, wind_up: int):
    time_left = best_time - wind_up
    my_dist = time_left * wind_up
    return my_dist > distance


def parse(data):
    lines = data.splitlines()
    times = [int(x) for x in lines[0].split(":")[-1].split()]
    distances = [int(x) for x in lines[1].split(":")[-1].split()]
    return times, distances

def parse2(data):
    lines = data.splitlines()
    time = int(''.join(lines[0].split(":")[-1].split()))
    dist = int(''.join(lines[1].split(":")[-1].split()))
    return time, dist


if __name__ == '__main__':
    prod = 1
    times, distances = parse(data)
    for time, dist in zip(times, distances):
        x = find_wins(time, dist)
        prod *= x
    print(prod)

    time, dist = parse2(data)
    x = find_wins(time, dist)
    print(x)
