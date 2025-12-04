import time

def digest():
    with open('2025/4/input.txt', 'r') as f:
        data = f.read().splitlines()
        data = [[char=='@' for char in line] for line in data]
    return data # List[List[bool]], 2D list of booleans

def count_surrounding_rolls(data, x, y, h, w):
    cnt = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue  # skip center

            nx = x + dx
            ny = y + dy

            if 0 <= nx < w and 0 <= ny < h:
                if data[ny][nx]:
                    cnt += 1
    return cnt


def part1(data):
    h = len(data)
    w = len(data[0])
    rolls = 0
    for y in range(h):
        for x in range(w):
            if not data[y][x]:
                continue

            if count_surrounding_rolls(data, x, y, h, w) < 4:
                rolls += 1

    return rolls

def count_removable_rolls(data, x, y, h, w):
    h = len(data)
    w = len(data[0])
    rolls = 0
    new_data = [row[:] for row in data]
    for y in range(h):
        for x in range(w):
            if not data[y][x]:
                continue

            if count_surrounding_rolls(data, x, y, h, w) < 4:
                rolls += 1
                new_data[y][x] = False

    return rolls, new_data

def part2(data):
    h = len(data)
    w = len(data[0])
    rolls = 0
    new_data = [row[:] for row in data]
    while True:
        removable, new_data = count_removable_rolls(new_data, 0, 0, h, w)
        if removable == 0:
            break
        rolls += removable

    return rolls


def main():
    data = digest()
    st = time.time()
    result_part1 = part1(data)
    print("part1:", result_part1)
    print("time:", time.time() - st)

    st = time.time()
    result_part2 = part2(data)
    print("part2:", result_part2)
    print("time:", time.time() - st)

if __name__ == '__main__':
    main()
