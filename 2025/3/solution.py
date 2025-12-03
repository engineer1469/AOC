import time

def digest():
    with open('2025/3/input.txt', 'r') as f:
        data = f.read().splitlines()
        #data = [[int(char) for char in line] for line in data]
    return data # List[List[int]], 2D list of integers


def GetMaxJoltage(bank, batteries):
    if batteries == 0:
        return ""

    # max index we are allowed to pick from
    limit = len(bank) - (batteries - 1)

    # pick the largest digit in the valid prefix
    max_digit = max(bank[:limit])
    idx = bank.index(max(bank[:limit]))

    # recurse on the remainder after that digit
    return max_digit + GetMaxJoltage(bank[idx+1:], batteries - 1)


def part1(data):
    joltagesum = 0
    for bank in data:
        joltage = GetMaxJoltage(bank, 2)
        joltagesum += int(joltage)
        
    return joltagesum

def part2(data):
    joltagesum = 0
    for bank in data:
        joltage = GetMaxJoltage(bank, 12)
        joltagesum += int(joltage)
        
    return joltagesum

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
