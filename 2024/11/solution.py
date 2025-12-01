import time
import math
from functools import lru_cache

def digest():
    with open('2024/11/input.txt', 'r') as f:
        data = [int(number) for number in f.read().split()]
    return data  # list of integers

def ENOD(n):
    return (math.floor(math.log10(abs(n))) + 1) % 2 == 0

def splitStone_values(n):
    stone_str = str(n)
    half = len(stone_str) // 2
    left = int(stone_str[:half]) if half > 0 else 0
    right = int(stone_str[half:]) if half < len(stone_str) else 0
    return left, right

@lru_cache(maxsize=None)
def count_stones(blinks, stone):
    if blinks == 0:
        return 1  # The stone itself remains
    
    if stone == 0:
        # Rule 1: Replace 0 with 1
        return count_stones(blinks - 1, 1)
    
    if ENOD(stone):
        # Rule 2: Split into two stones
        left, right = splitStone_values(stone)
        return count_stones(blinks - 1, left) + count_stones(blinks - 1, right)
    else:
        # Rule 3: Multiply by 2024
        new_stone = stone * 2024
        return count_stones(blinks - 1, new_stone)

def part_count(data, total_blinks):
    total = 0
    for stone in data:
        total += count_stones(total_blinks, stone)
    return total

def main():
    data = digest()
    
    total_blinks_part1 = 25
    st = time.time()
    result_part1 = part_count(data, total_blinks_part1)
    print(f"part1: {result_part1}")
    print(f"time for part1: {time.time() - st:.4f} seconds")
    
    total_blinks_part2 = 75
    st = time.time()
    result_part2 = part_count(data, total_blinks_part2)
    print(f"part2: {result_part2}")
    print(f"time for part2: {time.time() - st:.4f} seconds")

if __name__ == '__main__':
    main()
