import time

def digest():
    with open('2025/9/input.txt', 'r') as f:
        data = f.read().splitlines()
        data = [tuple(map(int, line.split(','))) for line in data]
    return data # List[(x,y)], list of 2D points

def part1(data):
    biggest_area = 0

    for i, (x1, y1) in enumerate(data):
        for j, (x2, y2) in enumerate(data):
            if i >= j:
                continue
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area > biggest_area:
                biggest_area = area

    return biggest_area


def point_in_polygon(px, py, polygon):
    n = len(polygon)
    inside = False
    
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        
        if ((y1 > py) != (y2 > py)): # ray is between y1 and y2
            # Calculate x-intersection point
            x_intersect = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if px < x_intersect:
                inside = not inside
    
    return inside


def segment_intersects_rect(x1, y1, x2, y2, rx_min, ry_min, rx_max, ry_max):
    if x1 == x2:# Vertical segment
        seg_x = x1
        seg_y_min, seg_y_max = min(y1, y2), max(y1, y2)
        if rx_min < seg_x < rx_max:  #inside x-range
            if seg_y_min < ry_max and seg_y_max > ry_min:  # Y range overlap
                return True
    else:# Horizontal segment
        seg_y = y1
        seg_x_min, seg_x_max = min(x1, x2), max(x1, x2)
        if ry_min < seg_y < ry_max:  #inside y-range
            if seg_x_min < rx_max and seg_x_max > rx_min:  # X range overlap
                return True
    return False


def is_box_contained(p1, p2, polygon):
    x_min = min(p1[0], p2[0])
    x_max = max(p1[0], p2[0])
    y_min = min(p1[1], p2[1])
    y_max = max(p1[1], p2[1])
    
    # Check if all 4 corners are inside the polygon
    corners = [
        (x_min, y_min),
        (x_min, y_max),
        (x_max, y_min),
        (x_max, y_max)
    ]
    
    for cx, cy in corners:
        if not point_in_polygon(cx, cy, polygon):
            return False
    
    # Check if no polygon edge intersects the rectangle edge
    n = len(polygon)
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        if segment_intersects_rect(x1, y1, x2, y2, x_min, y_min, x_max, y_max):
            return False
    
    return True


def part2(data):
    biggest_area = 0

    for i, (x1, y1) in enumerate(data):
        for j, (x2, y2) in enumerate(data):
            if i >= j:
                continue
            area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
            if area > biggest_area and is_box_contained((x1, y1), (x2, y2), data):
                biggest_area = area

    return biggest_area

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
