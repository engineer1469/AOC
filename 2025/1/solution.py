import time

def digest():
    with open('2025/1/input.txt', 'r') as f:
        data = f.read().splitlines()
        res = []
        for entry in data:
            if entry == '':
                break
            if entry[0] == 'L':
                res.append(-1*int(entry[1:]))
            else:
                res.append(int(entry[1:]))
                
    return res

def part1(data):
    pos = 50
    zeros = 0
    for move in data:
        pos += move
        pos = pos % 100
        if pos == 0:
            zeros += 1
    return zeros
    
def part2(data):
    pos = 50
    zeros = 0
    for move in data:
        new_pos = pos + move
        if move > 0:
            start = pos
            end = new_pos
            zeros += end // 100 - start // 100
        else:
            start = new_pos
            end = pos
            zeros += (end - 1) // 100 - (start - 1) // 100
        
        pos = new_pos % 100
    return zeros

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
