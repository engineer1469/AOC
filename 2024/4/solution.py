import re

def digest():
    with open('2024/4/input.txt', 'r') as f:
        data = f.read().splitlines()
        data = [list(line) for line in data]
    return data

def findStrings(String):
    pattern = re.compile(r'XMAS')
    matches = list(pattern.finditer(String))
    matches += list(pattern.finditer(String[::-1])) #find the matches in reverse
    return matches

def findHorizontal(data):
    count = 0
    for i in data:
        #convert the list to a string
        i = ''.join(i)
        #find the matches
        matches = findStrings(i)
        for match in matches:
            count += 1
    return count

def shiftArray(data):
    shifted = []
    #add all the lines with starting point on the horizontal axis
    for i in range(len(data[0])):
        diagonal = []
        for j in range(i, len(data)):
            diagonal.append(data[j][j-i])
        shifted.append(diagonal)
    #add all the lines with starting point on the vertical axis
    for i in range(1, len(data)):
        diagonal = []
        for j in range(i, len(data)):
            diagonal.append(data[j-i][j])
        shifted.append(diagonal)

    return shifted

def has_mas_diagonal(grid, x, y, dx, dy):
    # Check for 'MAS' or 'SAM' along the diagonal passing through (x,y) in direction (dx, dy)
    seq = []
    for i in [-1, 0, 1]:
        xi = x + i * dx
        yi = y + i * dy
        if 0 <= xi < len(grid[0]) and 0 <= yi < len(grid):
            seq.append(grid[yi][xi])
        else:
            return False
    return (seq == ['M', 'A', 'S'] or seq == ['S', 'A', 'M'] or
            seq[::-1] == ['M', 'A', 'S'] or seq[::-1] == ['S', 'A', 'M'])

def test_x_mas(grid, x, y):
    # Check both diagonals passing through (x, y)
    return has_mas_diagonal(grid, x, y, 1, 1) and has_mas_diagonal(grid, x, y, 1, -1)

    

def part1(data):
    horizontals = findHorizontal(data)
    verticals = findHorizontal(list(map(list, zip(*data))))#transpose the data
    #find the diagonals from the top left to the bottom right
    diagonals = findHorizontal(shiftArray(data))
    #find the diagonals from the top right to the bottom left
    diagonals += findHorizontal(shiftArray(data[::-1]))
    return horizontals + verticals + diagonals

def part2(grid):
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if test_x_mas(grid, x, y):
                count += 1
    return count


def main():
    data = digest()
    print("part1: ",part1(data))
    print("part2: ",part2(data))
    

if __name__ == '__main__':
    main()