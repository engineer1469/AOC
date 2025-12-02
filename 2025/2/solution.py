import time

def digest():
    with open('2025/2/input.txt', 'r') as f:
        data = f.read().split(',')
        data = [(int(x.split('-')[0]), int(x.split('-')[1])) for x in data]
    return data # List[(begin,end)], array of tuples

def isInvalid(num):
    s = str(num)
    if len(s)%2 != 0: # must be even length
        return False 
    half = len(s)//2
    # check first half == second half
    return s[:half] == s[half:]

def isInvalid2(num):
    s = str(num)
    length = len(s)
    # Only check substring lengths that divide evenly into the string length
    for sub_len in range(1, length):
        if length % sub_len == 0:
            sub = s[:sub_len]
            if sub * (length // sub_len) == s:
                return True
    return False

def sumInvalidInRange(begin, end):
    sum = 0
    for num in range(begin, end + 1):
        if isInvalid(num):
            sum += num
    return sum

def sumInvalidInRange2(begin, end):
    sum = 0
    for num in range(begin, end + 1):
        if isInvalid2(num):
            sum += num
    return sum

def part1(data):
    total_invalid = 0
    for begin, end in data:
        total_invalid += sumInvalidInRange(begin, end)
    return total_invalid


def part2(data):
    total_invalid = 0
    for begin, end in data:
        total_invalid += sumInvalidInRange2(begin, end)
    return total_invalid

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
