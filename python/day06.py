import math
data = """Time:        40     81     77     72
Distance:   219   1012   1365   1089"""

def count_wins(best_time: int, distance: int):
    return find_last(best_time, distance) - find_first(best_time, distance) + 1

def find_first(best_time: int, distance: int):
    check = 1
    step = best_time // 2
    while True:
        check_win = is_win(best_time, distance, check)
        plus_one = is_win(best_time, distance, check + 1)
        if not check_win and plus_one:
            return check + 1

        step = math.ceil(step / 2)
        if check_win:
            check -= step
        else:
            check += step

def find_last(best_time: int, distance: int):
    check = best_time
    step = best_time // 2
    while True:
        check_win = is_win(best_time, distance, check)
        minus_one = is_win(best_time, distance, check - 1)
        if not check_win and minus_one:
            return check - 1

        step = math.ceil(step / 2)
        if check_win:
            check += step
        else:
            check -= step

def is_win(best_time: int, distance: int, wind_up: int):
    return (best_time - wind_up) * wind_up > distance

def parse(data):
    lines = data.splitlines()
    times = [int(x) for x in lines[0].split(":")[-1].split()]
    distances = [int(x) for x in lines[1].split(":")[-1].split()]
    return times, distances

if __name__ == '__main__':
    times, distances = parse(data)
    print(math.prod(count_wins(time, dist) for time, dist in zip(times, distances)))
    time, dist = int(''.join(map(str, times))), int(''.join(map(str, distances)))
    print(count_wins(time, dist))
