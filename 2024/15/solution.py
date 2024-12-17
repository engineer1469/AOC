import time
import copy

def digest():
    with open('2024/15/input.txt', 'r') as f:
        lines = f.read().splitlines()
    
    map_lines = []
    instruction_lines = []
    reading_map = True
    
    for line in lines:
        if not line.strip():
            reading_map = False
            continue
        if reading_map:
            map_lines.append(list(line))
        else:
            instruction_lines.append(line.strip())
    
    instructions = list(''.join(instruction_lines))
    
    return map_lines, instructions

def simulate_moves(warehouse_map, move_instructions):
    # Find the robot's initial position
    robot_pos = None
    for r, row in enumerate(warehouse_map):
        for c, val in enumerate(row):
            if val == '@':
                robot_pos = (r, c)
                break
        if robot_pos:
            break
        
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }
    
    def can_push(r, c, dr, dc):
        next_r, next_c = r + dr, c + dc
        if warehouse_map[next_r][next_c] == '#':
            return False  # Wall blocks the push
        if warehouse_map[next_r][next_c] == 'O':
            # Another box is in the way; attempt to push it
            return can_push(next_r, next_c, dr, dc)
        # Empty space; can push
        return True
    
    def push_box(r, c, dr, dc):
        next_r, next_c = r + dr, c + dc
        if warehouse_map[next_r][next_c] == 'O':
            # Push the next box first
            push_box(next_r, next_c, dr, dc)
        # Move the current box
        warehouse_map[next_r][next_c] = 'O'
        warehouse_map[r][c] = '@' if (r, c) == robot_pos else 'O'
    
    for move in move_instructions:
        if move not in directions:
            continue  # Ignore invalid instructions
        
        dr, dc = directions[move]
        new_r, new_c = robot_pos[0] + dr, robot_pos[1] + dc
        
        # Check boundaries (assuming the map is surrounded by walls)
        if new_r < 0 or new_r >= len(warehouse_map) or new_c < 0 or new_c >= len(warehouse_map[0]):
            continue  # Movement out of bounds; ignore
        
        target_cell = warehouse_map[new_r][new_c]
        
        if target_cell == '#':
            continue  # Movement blocked by wall
        
        elif target_cell == 'O':
            # Attempt to push the box
            if can_push(new_r, new_c, dr, dc):
                push_box(new_r, new_c, dr, dc)
                
                # After pushing, check what was at the robot's original position
                warehouse_map[robot_pos[0]][robot_pos[1]] = '.'  # Assume empty space
                
                # Move the robot
                warehouse_map[new_r][new_c] = '@'
                robot_pos = (new_r, new_c)
            else:
                continue  # Can't push the box; movement blocked
        
        else:
            # Move the robot
            warehouse_map[new_r][new_c] = '@'
            warehouse_map[robot_pos[0]][robot_pos[1]] = '.'  # Assume empty space
            robot_pos = (new_r, new_c)

    return calculate_GPS(warehouse_map)

def calculate_GPS(warehouse_map):
    gps_sum = 0
    for r, row in enumerate(warehouse_map):
        for c, val in enumerate(row):
            if val == 'O' or val == '[':
                gps_sum += 100 * r + c
    
    return gps_sum

def scale_map_part2(original_map):
    substitution = {
        '#': ['#', '#'],
        'O': ['[', ']'],
        '.': ['.', '.'],
        '@': ['@', '.']
    }
    
    scaled_map = []
    
    for row_index, row in enumerate(original_map):
        new_row = []
        for col_index, char in enumerate(row):
            # Get the substitution for the current character
            substituted_chars = substitution.get(char, [char, char])
            new_row.extend(substituted_chars)
        
        scaled_map.append(new_row)
    
    return scaled_map

def part1():
    data = digest()
    warehouse_map, instructions = data
    return simulate_moves(warehouse_map, instructions)

def part2():
    data = digest()
    warehouse_map, instructions = data
    scaled_map = scale_map_part2(warehouse_map)
    return simulate_moves_part2(scaled_map, instructions)
    
def main():
    # Part 1
    st = time.time()
    result_part1 = part1()
    print("part1:", result_part1)
    print("time:", time.time() - st)

    # Part 2
    st = time.time()
    result_part2 = part2()
    print("part2:", result_part2)
    print("time:", time.time() - st)

if __name__ == '__main__':
    main()
