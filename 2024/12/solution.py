import time
import copy
from collections import deque, defaultdict

def digest():
    with open('2024/12/input.txt', 'r') as f:
        data = f.read().splitlines()
        data = [[char for char in line] for line in data]
    return data  # List[List[str]], 2D list of characters

def findRegions(data):
    height = len(data)
    width = len(data[0]) if height > 0 else 0
    visited = set()
    regions = []
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    
    for y in range(height):
        for x in range(width):
            if (x, y) not in visited:
                symbol = data[y][x]
                region = set()
                queue = deque([(x, y)])
                visited.add((x, y))

                while queue:
                    cx, cy = queue.popleft()
                    region.add((cx, cy))

                    for dx, dy in directions:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if data[ny][nx] == symbol and (nx, ny) not in visited:
                                visited.add((nx, ny))
                                queue.append((nx, ny))
                regions.append(region)
    return regions

def part1(data):
    data = copy.deepcopy(data)
    regions = findRegions(data)
    height = len(data)
    width = len(data[0]) if height > 0 else 0

    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    total_price = 0
    for region in regions:
        any_point = next(iter(region))
        x0, y0 = any_point
        symbol = data[y0][x0]

        area = len(region)
        perimeter = 0
        for (cx, cy) in region:
            for dx, dy in directions:
                nx, ny = cx+dx, cy+dy
                if not (0 <= nx < width and 0 <= ny < height and (nx, ny) in region and data[ny][nx] == symbol):
                    perimeter += 1
        price = area * perimeter
        total_price += price
    return total_price

N, E, S, W = 'N','E','S','W'

def getEdges(region, data):
    edges = set()
    height = len(data)
    width = len(data[0]) if height > 0 else 0

    for (x, y) in region:
        # Check north
        if y == 0 or (x, y-1) not in region:
            edges.add((x, y, N))
        # Check south
        if y == height - 1 or (x, y+1) not in region:
            edges.add((x, y, S))
        # Check west
        if x == 0 or (x-1, y) not in region:
            edges.add((x, y, W))
        # Check east
        if x == width - 1 or (x+1, y) not in region:
            edges.add((x, y, E))

    return edges

def followPolygon(edges, size):
    edges = set(edges)
    sides_count = 0

    while edges:
        start = next(iter(edges))
        (x, y, facing) = start
        first = True
        loop_start = (x, y, facing)
        while True:
            if first:
                first = False
            else:
                if (x, y, facing) in edges:
                    edges.remove((x, y, facing))
            if facing == N:
                if x > 0 and (x-1, y, N) in edges:
                    x -= 1
                elif x > 0 and y > 0 and (x-1, y-1, E) in edges:
                    sides_count += 1
                    x -= 1
                    y -= 1
                    facing = E
                elif (x, y, W) in edges:
                    sides_count += 1
                    facing = W
                else:
                    break

            elif facing == E:
                if y > 0 and (x, y-1, E) in edges:
                    y -= 1
                elif y > 0 and x < size - 1 and (x+1, y-1, S) in edges:
                    sides_count += 1
                    x += 1
                    y -= 1
                    facing = S
                elif (x, y, N) in edges:
                    sides_count += 1
                    facing = N
                else:
                    break

            elif facing == S:
                if x < size - 1 and (x+1, y, S) in edges:
                    x += 1
                elif x < size - 1 and y < size - 1 and (x+1, y+1, W) in edges:
                    sides_count += 1
                    x += 1
                    y += 1
                    facing = W
                elif (x, y, E) in edges:
                    sides_count += 1
                    facing = E
                else:
                    break

            elif facing == W:
                if y < size - 1 and (x, y+1, W) in edges:
                    y += 1
                elif y < size - 1 and x > 0 and (x-1, y+1, N) in edges:
                    sides_count += 1
                    x -= 1
                    y += 1
                    facing = N
                elif (x, y, S) in edges:
                    sides_count += 1
                    facing = S
                else:
                    break

    return sides_count

def part2(data):
    data = copy.deepcopy(data)
    regions = findRegions(data)
    total_price = 0
    height = len(data)
    size = height

    for region in regions:
        edges = getEdges(region, data)
        sides = followPolygon(edges, size)
        area = len(region)
        price = area * sides
        total_price += price

    return total_price

def main():
    data = digest()

    # Part 1
    st = time.time()
    result_part1 = part1(data)
    print("part1:", result_part1)
    print("time:", time.time() - st)

    # Part 2
    st = time.time()
    result_part2 = part2(data)
    print("part2:", result_part2)
    print("time:", time.time() - st)

if __name__ == '__main__':
    main()
