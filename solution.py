import time

def digest():
    with open('2024/10/input.txt', 'r') as f:
        data = f.read().splitlines()
        data = [[int(char) for char in line] for line in data]
    return data # List[List[int]], 2D list of integers

def part1(data):
    pass

def part2(data):
    pass

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
