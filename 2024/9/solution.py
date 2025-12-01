import time
import copy

def digest():
    with open('2024/9/input.txt', 'r') as f:
        data = f.read().strip()
        data = [int(char) for char in data]
    return data

def decompress(data):
    decompressed = []
    i = 0
    id = 0
    while i < len(data):
        part = []
        if i%2 == 0:
            part = [id]*data[i]
            id += 1
            decompressed.extend(part)
        else:
            part = ['.']*data[i]
            decompressed.extend(part)
        i += 1
    
    return decompressed

def compact(data):
    compacted = copy.deepcopy(data)
    while True:
        while compacted[-1] == '.':
            compacted.pop()
        if '.' not in compacted:
            break
        id1 = compacted.index('.')
        id2 = len(compacted) - 1
        compacted[id1], compacted[id2] = compacted[id2], compacted[id1]

    return compacted

def checksum(data):
    total = 0
    for i in range(len(data)):
        if data[i] not in (None, '.'):
            total += int(data[i]) * i
    return total

def part1(data):
    decompressed = decompress(data)
    compacted = compact(decompressed)
    return checksum(compacted)

def part2(data):
    decompressed = decompress(data)
    ans = [None] * len(decompressed)
    used_data = []
    free_data = []

    is_space = False
    pos = 0
    for v in data:
        if is_space:
            free_data.append([pos, v])
            for _ in range(v):
                ans[pos] = None
                pos += 1
        else:
            fid = len(used_data)
            used_data.append([pos, v, fid])
            for _ in range(v):
                ans[pos] = fid
                pos += 1
        is_space = not is_space

    for file in sorted(used_data, key=lambda x: -x[2]):
        idx, size, fid = file
        target = next(
            (fs for fs in free_data if fs[0] < idx and size <= fs[1]),
            None,
        )
        if target:
            free_start, free_length = target
            for i in range(size):
                ans[idx + i] = None
                ans[free_start + i] = fid
            target[0] += size
            target[1] -= size

    return checksum(ans)


def main():
    data = digest()
    #data = [2,3,3,3,1,3,3,1,2,1,4,1,4,1,3,1,4,0,2]
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
