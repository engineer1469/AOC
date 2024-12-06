import time
from concurrent.futures import ProcessPoolExecutor

def digest():
    with open('2024/6/input.txt') as f:
        # Convert puzzle into a 2D array of chars
        puzzle = [list(line.strip()) for line in f]
    return puzzle

def pathArrayToFile(pathArray):
    with open('2024/6/path.txt', 'w') as f:
        for line in pathArray:
            f.write(''.join(line) + '\n')

def countPath(pathArray):
    count = 0
    for line in pathArray:
        for char in line:
            if char == 'X':
                count += 1
    return count

def part1(data):
    data = [list(line) for line in data]
    pathArray = [list(line) for line in data]

    location = [0, 0]  # [y, x]
    direction = [-1, 0]  # facing up
    visited_positions = []
    start_found = False

    # Find the '^' position
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '^':
                location = [y, x]
                data[y][x] = '.'
                visited_positions.append((y, x))
                start_found = True
                break
        if start_found:
            break

    while True:
        ny = location[0] + direction[0]
        nx = location[1] + direction[1]

        # Check if next step is out of bounds
        if nx < 0 or nx >= len(data[0]) or ny < 0 or ny >= len(data):
            count = countPath(pathArray)
            return count, visited_positions

        # If there's an obstacle directly in front, turn right (90° clockwise)
        if data[ny][nx] == '#':
            direction = [direction[1], -direction[0]]

        if data[ny][nx] == '.':
            location = [ny, nx]
            pathArray[ny][nx] = 'X'
            visited_positions.append((ny, nx))

def test_for_loop(data, start_y, start_x, obst_y=None, obst_x=None):
    y, x = start_y, start_x
    direction = [-1, 0]  # facing up
    visited_states = set()  # set of (y, x, dy, dx)

    rows = len(data)
    cols = len(data[0])

    while True:
        state = (y, x, direction[0], direction[1])
        if state in visited_states:
            # Loop detected
            return True
        visited_states.add(state)

        ny = y + direction[0]
        nx = x + direction[1]

        # Check bounds
        if nx < 0 or nx >= cols or ny < 0 or ny >= rows:
            return False

        # Determine what is at the next cell
        # If it's the obstruction cell, treat as '#', else use data
        cell = '#'
        if not (obst_y == ny and obst_x == nx):
            cell = data[ny][nx]

        if cell == '#':
            # Rotate direction right
            direction = [direction[1], -direction[0]]
        else:
            # Move forward
            y, x = ny, nx

def check_obstruction(args):
    vy, vx, data, start_y, start_x = args
    # Test with obstruction at (vy, vx)
    return test_for_loop(data, start_y, start_x, obst_y=vy, obst_x=vx)

def part2(data):
    result, visited_positions = part1(data)
    start_y, start_x = visited_positions[0]

    unique_positions = set(visited_positions[1:])
    tasks = [(vy, vx, data, start_y, start_x) for (vy, vx) in unique_positions
             if (vy, vx) != (start_y, start_x)]

    loop_count = 0
    with ProcessPoolExecutor() as executor:
        for is_loop in executor.map(check_obstruction, tasks):
            if is_loop:
                loop_count += 1

    return loop_count

def main():
    data = digest()
    st = time.time()
    print("part1: ", part1(data)[0])
    print("time: ", time.time() - st)

    st = time.time()
    print("part2: ", part2(data))
    print("time: ", time.time() - st)

if __name__ == '__main__':
    main()
