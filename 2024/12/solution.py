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
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
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
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    total_price = 0
    
    for region in regions:
        # Determine symbol from any cell in region
        any_point = next(iter(region))
        x0, y0 = any_point
        symbol = data[y0][x0]

        area = len(region)
        perimeter = 0
        
        for (cx, cy) in region:
            # Check each of the four sides for perimeter contribution
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < width and 0 <= ny < height and data[ny][nx] == symbol and (nx, ny) in region):
                    perimeter += 1

        price = area * perimeter
        total_price += price

    return total_price

def getCellEdges(region, data, x, y):
    height = len(data)
    width = len(data[0]) if height > 0 else 0
    
    edges = []
    
    # Top edge
    if y == 0 or (x, y-1) not in region:
        edges.append(('H', y, x))
    # Bottom edge
    if y == height - 1 or (x, y+1) not in region:
        edges.append(('H', y+1, x))
    # Left edge
    if x == 0 or (x-1, y) not in region:
        edges.append(('V', x, y))
    # Right edge
    if x == width - 1 or (x+1, y) not in region:
        edges.append(('V', x+1, y))
    
    return edges

def findHorizontalSides(horizontal_edges):
    sides = 0
    # Group by y
    by_y = defaultdict(list)
    for (_, y, x) in horizontal_edges:
        by_y[y].append(x)
    
    for y, xs in by_y.items():
        xs.sort()
        # Count contiguous runs in xs
        start = xs[0]
        prev = xs[0]
        for i in range(1, len(xs)):
            if xs[i] != prev + 1:
                # Gap found, one side ended
                sides += 1
                start = xs[i]
            prev = xs[i]
        # End the last run
        sides += 1
    return sides

def findVerticalSides(vertical_edges):
    sides = 0
    # Group by x
    by_x = defaultdict(list)
    for (_, x, y) in vertical_edges:
        by_x[x].append(y)
    
    for x, ys in by_x.items():
        ys.sort()
        # Count contiguous runs in ys
        start = ys[0]
        prev = ys[0]
        for i in range(1, len(ys)):
            if ys[i] != prev + 1:
                # Gap found, one side ended
                sides += 1
                start = ys[i]
            prev = ys[i]
        # End the last run
        sides += 1
    return sides

def part2(data):
    data = copy.deepcopy(data)
    regions = findRegions(data)
    total_price = 0
    
    for region in regions:
        # Collect edges for this region
        horizontal_edges = set()
        vertical_edges = set()
        
        for (x, y) in region:
            cell_edges = getCellEdges(region, data, x, y)
            for e in cell_edges:
                if e[0] == 'H':
                    horizontal_edges.add(e)
                else:
                    vertical_edges.add(e)
        
        h_sides = findHorizontalSides(horizontal_edges)
        v_sides = findVerticalSides(vertical_edges)
        
        sides = h_sides + v_sides
        
        # Price = area * sides
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
