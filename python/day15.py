from pathlib import Path

data = (Path(__file__).parent.parent / "data" / "day15.txt").read_text()


HASHMAP = [[] for _ in range(257)]

def do_hash(item: str):
    val = 0
    for ch in item:
        val += ord(ch)
        val *= 17
    return val % 256


if __name__ == "__main__":
    data = data.strip().split(",")
    total = 0
    for line in data:
        total += do_hash(line)
    print(total)


    for line in data:
        if '=' in line:
            label, focal = line.split('=')
            focal = int(focal)
            idx = do_hash(label)
            try:
                i = [x[0] for x in HASHMAP[idx]].index(label)
                HASHMAP[idx][i] = (label, focal)
            except ValueError:
                HASHMAP[idx].append((label, focal))
        elif '-' in line:
            label = line.rstrip('-')
            idx = do_hash(label)
            try:
                i = [x[0] for x in HASHMAP[idx]].index(label)
                del HASHMAP[idx][i]
            except ValueError:
                pass

    focusing_power = 0
    for i, box in enumerate(HASHMAP):
        for j, (label, focal) in enumerate(box, 1):
            focusing_power += (i + 1) * focal * j
    print(focusing_power)
