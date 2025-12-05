import time

def digest():
    with open('2025/5/input.txt', 'r') as f:
        input = f.read().split('\n\n')
        ranges = input[0].splitlines()
        database = []
        for r in ranges:
            start, end = r.split('-')
            # Create a ranges list of tuples (begin, end)
            for range in ranges:
                start, end = range.split('-')
                database.append((int(start), int(end)))

        ids = input[1].splitlines()
        ids = [int(x) for x in ids]

    return database, ids

def merge_ranges(ranges):
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged = []
    for range in sorted_ranges:
        if not merged or merged[-1][1] < range[0]:
            merged.append(range)
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], range[1]))
    return merged

def part1(database, ids):
    count = 0
    for id in ids:
        for start, end in database:
            if start <= id <= end:
                count += 1
                break
    return count

def part2(database):
    count = 0
    for range in database:
        start, end = range
        count += (end - start + 1)
    return count

def main():
    database, ids = digest()
    database = merge_ranges(database)
    st = time.time()
    result_part1 = part1(database, ids)
    print("part1:", result_part1)
    print("time:", time.time() - st)

    st = time.time()
    result_part2 = part2(database)
    print("part2:", result_part2)
    print("time:", time.time() - st)

if __name__ == '__main__':
    main()
