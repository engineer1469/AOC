import time
import heapq

def digest():
    with open('2024/16/input.txt', 'r') as f:
        lines = f.read().splitlines()
        lines = [list(line) for line in lines]
    return lines  # 2D array of chars

def part1(data):
    DIRECTIONS = ['East', 'South', 'West', 'North']
    DIR_MAP = {
        'East': (1, 0),
        'South': (0, 1),
        'West': (-1, 0),
        'North': (0, -1)
    }

    start = None
    end = None
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == 'S':
                start = (x, y)
            elif value == 'E':
                end = (x, y)

    start_x, start_y = start
    initial_direction = 'East'
    heap = [(0, start_x, start_y, initial_direction)]
    visited = {}

    while heap:
        current_score, x, y, direction = heapq.heappop(heap)

        if (x, y) == end:
            return current_score  # minimal score to reach E

        # Skip if we have found a better way before
        if (x, y, direction) in visited and visited[(x, y, direction)] <= current_score:
            continue

        visited[(x, y, direction)] = current_score

        # Move Forward
        dx, dy = DIR_MAP[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_y < len(data) and 0 <= new_x < len(data[0]) and data[new_y][new_x] != '#':
            heapq.heappush(heap, (current_score + 1, new_x, new_y, direction))

        # Rotate Left
        cdi = DIRECTIONS.index(direction)
        new_dir_left = DIRECTIONS[(cdi - 1) % 4]
        heapq.heappush(heap, (current_score + 1000, x, y, new_dir_left))

        # Rotate Right
        new_dir_right = DIRECTIONS[(cdi + 1) % 4]
        heapq.heappush(heap, (current_score + 1000, x, y, new_dir_right))

    return -1  # No path found

def compute_all_costs(data):
    DIRECTIONS = ['East', 'South', 'West', 'North']
    DIR_MAP = {
        'East': (1, 0),
        'South': (0, 1),
        'West': (-1, 0),
        'North': (0, -1)
    }

    start = None
    end = None
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == 'S':
                start = (x, y)
            elif value == 'E':
                end = (x, y)
    if not start or not end:
        raise ValueError("Start 'S' or End 'E' not found in the data.")

    start_x, start_y = start
    initial_direction = 'East'
    heap = [(0, start_x, start_y, initial_direction)]
    visited = {}

    DIRECTIONS_MAP = {
        'East': (1, 0),
        'South': (0, 1),
        'West': (-1, 0),
        'North': (0, -1)
    }

    while heap:
        current_score, x, y, direction = heapq.heappop(heap)

        if (x, y, direction) in visited and visited[(x, y, direction)] <= current_score:
            continue

        visited[(x, y, direction)] = current_score

        # Move Forward
        dx, dy = DIRECTIONS_MAP[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_y < len(data) and 0 <= new_x < len(data[0]) and data[new_y][new_x] != '#':
            heapq.heappush(heap, (current_score + 1, new_x, new_y, direction))

        # Rotate Left
        cdi = DIRECTIONS.index(direction)
        new_dir_left = DIRECTIONS[(cdi - 1) % 4]
        heapq.heappush(heap, (current_score + 1000, x, y, new_dir_left))

        # Rotate Right
        new_dir_right = DIRECTIONS[(cdi + 1) % 4]
        heapq.heappush(heap, (current_score + 1000, x, y, new_dir_right))

    return visited

def part2(data):
    # First, compute all minimal costs
    visited = compute_all_costs(data)

    # Identify start and end
    start = None
    end = None
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == 'S':
                start = (x, y)
            elif value == 'E':
                end = (x, y)
    if not start or not end:
        return 0

    # Find minimal score to E and all end states with that minimal score
    min_score = float('inf')
    end_states = []
    for (x, y, direction), score in visited.items():
        if (x, y) == end:
            if score < min_score:
                min_score = score
                end_states = [(x, y, direction)]
            elif score == min_score:
                end_states.append((x, y, direction))

    if min_score == float('inf'):
        # No path to E
        return 0

    # Now perform a reverse BFS. We know the minimal costs. We find predecessors by cost relations.
    DIRECTIONS = ['East', 'South', 'West', 'North']
    DIR_MAP = {
        'East': (1, 0),
        'South': (0, 1),
        'West': (-1, 0),
        'North': (0, -1)
    }

    tiles_on_optimal_paths = set()
    queue = end_states[:]
    visited_back = set()

    while queue:
        cx, cy, cdir = queue.pop()
        if (cx, cy, cdir) in visited_back:
            continue
        visited_back.add((cx, cy, cdir))

        tiles_on_optimal_paths.add((cx, cy))
        c_cost = visited[(cx, cy, cdir)]
        dx, dy = DIR_MAP[cdir]
        px, py = cx - dx, cy - dy
        if (px, py, cdir) in visited and visited[(px, py, cdir)] + 1 == c_cost:
            queue.append((px, py, cdir))
        cdi = DIRECTIONS.index(cdir)

        # Rotate right predecessor:
        pdir_right = DIRECTIONS[(cdi - 1) % 4]
        if (cx, cy, pdir_right) in visited and visited[(cx, cy, pdir_right)] + 1000 == c_cost:
            queue.append((cx, cy, pdir_right))

        # rotate left predecessor:
        pdir_left = DIRECTIONS[(cdi + 1) % 4]
        if (cx, cy, pdir_left) in visited and visited[(cx, cy, pdir_left)] + 1000 == c_cost:
            queue.append((cx, cy, pdir_left))

    # mark these tiles
    for (x, y) in tiles_on_optimal_paths:
        if data[y][x] not in ['S', 'E']:
            data[y][x] = 'O'

    save_to_output(data)
    return len(tiles_on_optimal_paths)

def save_to_output(data):
    with open('2024/16/output.txt', 'w') as f:
        for row in data:
            f.write(''.join(row) + '\n')

def main():
    data = digest()
    
    st = time.time()
    result_part1 = part1(data)
    print("part1:", result_part1)
    print("time:", time.time() - st, "seconds")

    data = digest()
    st = time.time()
    result_part2 = part2(data)
    print("\npart2:", result_part2)
    print("time:", time.time() - st, "seconds")

if __name__ == '__main__':
    main()
