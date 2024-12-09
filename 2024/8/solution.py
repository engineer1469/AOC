import time
import math

def digest():
    with open('2024/8/input.txt', 'r') as f:
        data = f.read().splitlines()
        data = [list(line) for line in data]
        global bounds #global variable to store the bounds of the grid
        bounds = [len(data[0]), len(data)]
    return data #2D array

def groupAntennas(data):
    antenna_dict = {}
    for i in range(len(data)):
        for j in range(len(data[i])):
            char = data[i][j]
            if char != '.':
                if char not in antenna_dict:
                    antenna_dict[char] = []
                antenna_dict[char].append([j, i])

    antennas = []
    for char, coords in antenna_dict.items():
        antennas.append([char, coords])
    return antennas

def calculateNodePositions(antennas):
    #calculate for every combination of 2 antennas, the position of the unique nodes that are in bounds
    nodes = []
    for i in range(len(antennas)):
        for j in range(i+1, len(antennas)):
            node1, node2 = calculateNodePosition(antennas[i][0], antennas[i][1], antennas[j][0], antennas[j][1])
            if node1[0] >= 0 and node1[0] < bounds[0] and node1[1] >= 0 and node1[1] < bounds[1]:
                nodes.append(node1)
            if node2[0] >= 0 and node2[0] < bounds[0] and node2[1] >= 0 and node2[1] < bounds[1]:
                nodes.append(node2)

    return nodes

def calculateNodePosition(xt1, yt1, xt2, yt2):
    diff = [xt2 - xt1, yt2 - yt1]
    node1 = [xt1-diff[0], yt1-diff[1]]
    node2 = [xt2+diff[0], yt2+diff[1]]
    return node1, node2 #returning [x,y] coordinates

def part1(data):
    antennas = groupAntennas(data)
    all_nodes = []
    for antennaGroup in antennas:
        coords = antennaGroup[1]
        nodes = calculateNodePositions(coords)
        all_nodes.extend(nodes)

    unique_nodes = set((x,y) for x,y in all_nodes)
    return len(unique_nodes)


def part2(data):
    antennas = groupAntennas(data)
    width, height = bounds
    antinodes = set()

    for freq, coords in antennas:
        if len(coords) < 2:
            # Only one antenna of this frequency, can't form a line
            continue
        # For each pair of antennas
        for i in range(len(coords)):
            x1, y1 = coords[i]
            for j in range(i+1, len(coords)):
                x2, y2 = coords[j]
                dx = x2 - x1
                dy = y2 - y1
                g = math.gcd(dx, dy)
                dx //= g
                dy //= g

                # Move forward from (x1, y1)
                fx, fy = x1, y1
                while 0 <= fx < width and 0 <= fy < height:
                    antinodes.add((fx, fy))
                    fx += dx
                    fy += dy
                
                # Move backward from (x1 - dx, y1 - dy)
                bx, by = x1 - dx, y1 - dy
                while 0 <= bx < width and 0 <= by < height:
                    antinodes.add((bx, by))
                    bx -= dx
                    by -= dy

    return len(antinodes)


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
