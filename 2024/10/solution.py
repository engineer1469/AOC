import time

def digest():
    with open('2024/10/input.txt', 'r') as f:
        data = f.read().splitlines()
        data = [[int(char) for char in line] for line in data]
    return data # List[List[int]], 2D list of integers

def findNext(data, x, y, visited):
    if (x, y) in visited:
        return set()
    visited.add((x, y))
    
    current = data[y][x]
    if current == 9:  # peak found
        return {(x, y)}
    
    peaks = set()
    # Move down
    if y + 1 < len(data) and data[y + 1][x] == current + 1:
        peaks |= findNext(data, x, y + 1, visited)
    # Move up
    if y - 1 >= 0 and data[y - 1][x] == current + 1:
        peaks |= findNext(data, x, y - 1, visited)
    # Move right
    if x + 1 < len(data[0]) and data[y][x + 1] == current + 1:
        peaks |= findNext(data, x + 1, y, visited)
    # Move left
    if x - 1 >= 0 and data[y][x - 1] == current + 1:
        peaks |= findNext(data, x - 1, y, visited)
    
    return peaks

def findNextWithDuplicates(data, x, y):
    current = data[y][x]
    if current == 9:  # Base case: peak reached
        return 1

    count = 0
    # Move down
    if y + 1 < len(data) and data[y + 1][x] == current + 1:
        count += findNextWithDuplicates(data, x, y + 1)
    # Move up
    if y - 1 >= 0 and data[y - 1][x] == current + 1:
        count += findNextWithDuplicates(data, x, y - 1)
    # Move right
    if x + 1 < len(data[0]) and data[y][x + 1] == current + 1:
        count += findNextWithDuplicates(data, x + 1, y)
    # Move left
    if x - 1 >= 0 and data[y][x - 1] == current + 1:
        count += findNextWithDuplicates(data, x - 1, y)

    return count

def part1(data):
    total_count = 0
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == 0:
                visited = set()
                peaks = findNext(data, x, y, visited)
                # Count how many unique peaks this zero can reach
                total_count += len(peaks)
    return total_count


def part2(data):
    total_rating = 0
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == 0:  # Start from every trailhead (zero)
                total_rating += findNextWithDuplicates(data, x, y)
    return total_rating

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
