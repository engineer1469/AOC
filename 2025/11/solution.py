import time
from functools import lru_cache

def str_to_int(s):
    # Convert 3-character string to base-26 number
    # "you" = 16608, "out" = 10003
    return (ord(s[0]) - ord('a')) * 676 + (ord(s[1]) - ord('a')) * 26 + (ord(s[2]) - ord('a'))

# Global for lru_cache access
CONNECTIONS = None
TARGET = None
DAC = None
FFT = None

def digest():
    with open('2025/11/input.txt', 'r') as f:
        connections = {}
        data = f.read().splitlines()
        for line in data:
            parts = line.split(': ')
            node = str_to_int(parts[0])
            neighbors = [str_to_int(n) for n in parts[1].split(' ')]
            connections[node] = neighbors
    return connections  # Dict[int, List[int]]

def dfs_count_paths(connections, current, target=None, visited=None):
    if target is None:
        target = str_to_int('out')
    if visited is None:
        visited = set()
    
    if current == target:
        return 1
    
    visited.add(current)
    total = 0
    for neighbor in connections.get(current, []):
        if neighbor not in visited:
            total += dfs_count_paths(connections, neighbor, target, visited)
    visited.remove(current)  # backtrack to allow other paths
    return total

@lru_cache(maxsize=None)
def dfs_cached(current, dac_seen, fft_seen):
    if current == DAC:
        dac_seen = True
    if current == FFT:
        fft_seen = True
    
    if current == TARGET:
        return 1 if (dac_seen and fft_seen) else 0
    
    total = 0
    for neighbor in CONNECTIONS.get(current, []):
        total += dfs_cached(neighbor, dac_seen, fft_seen)
    return total

def dfs_count_paths_dac_and_fft(connections, current):
    global CONNECTIONS, TARGET, DAC, FFT
    CONNECTIONS = connections
    TARGET = str_to_int('out')
    DAC = str_to_int('dac')
    FFT = str_to_int('fft')
    dfs_cached.cache_clear()
    return dfs_cached(current, False, False)

def part1(data):
    count = 0
    start = str_to_int('you')
    count += dfs_count_paths(data, start)

    return count

def part2(data):
    start = str_to_int('svr')
    return dfs_count_paths_dac_and_fft(data, start)

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
