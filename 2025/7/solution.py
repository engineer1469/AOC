import time

def digest():
    with open('2025/7/input.txt', 'r') as f:
        data = f.read().splitlines()
        #data = [[int(char) for char in line] for line in data]
        #replace 'S' with '|' in the first line
        data[0] = data[0].replace('S', '|')
    return data

def part1(data):
    data = [list(line) for line in data]
    
    count = 0
    i = 1
    while i < len(data):
        for index, char in enumerate(data[i]):
            
            if char == '.' and data[i-1][index] == '|':
                data[i][index] = '|'

            elif char == '^' and data[i-1][index] == '|':
                data[i][index-1] = '|'
                data[i][index+1] = '|'
                count += 1

        i += 1
    return count

def part2(data):
    pattern = [list(line) for line in data]
    rows = len(data)
    cols = len(data[0])
    
    # Create a separate grid for timeline counts
    values = [[0] * cols for _ in range(rows)]
    
    # Initialize the starting position with 1
    for index, char in enumerate(pattern[0]):
        if char == '|':
            values[0][index] = 1
    
    # Process each row
    for i in range(1, rows):
        for index in range(cols):
            char = pattern[i][index]
            above = values[i-1][index]

            if char == '.' and above > 0:
                values[i][index] += above

            elif char == '^' and above > 0:
                # Split left and right
                values[i][index-1] += above
                values[i][index+1] += above

    return sum(values[-1])

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
