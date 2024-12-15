import os
import re
from PIL import Image, ImageDraw
import time

def digest(file_path="2024/14/input.txt"):
    robots = []
    pattern = re.compile(r"p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)")

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            x, y, vx, vy = map(int, match.groups())
            robots.append(((x, y), (vx, vy)))
    return robots

def tick(robot, width=101, height=103):
    (x, y), (vx, vy) = robot
    return (((x + vx) % width, (y + vy) % height), (vx, vy))

def count_quadrants(data, width=101, height=103):
    mid_x = width // 2.0
    mid_y = height // 2.0
    q1 = q2 = q3 = q4 = 0

    for (x, y), _ in data:
        if x < mid_x and y < mid_y:
            q1 += 1  # top-left
        elif x > mid_x and y < mid_y:
            q2 += 1  # top-right
        elif x < mid_x and y > mid_y:
            q3 += 1  # bottom-left
        elif x > mid_x and y > mid_y:
            q4 += 1  # bottom-right

    return q1, q2, q3, q4

def save_floor_image(data, width=101, height=103, folder="pictures", step=0, scale=5):
    # Ensure the pictures folder exists
    os.makedirs(folder, exist_ok=True)

    # Define image size with scaling
    img_width = width * scale
    img_height = height * scale

    # Create a new white image
    image = Image.new('RGB', (img_width, img_height), color='black')
    draw = ImageDraw.Draw(image)

    # Draw robots as white squares
    for (x, y), _ in data:
        top_left = (x * scale, y * scale)
        bottom_right = ((x + 1) * scale - 1, (y + 1) * scale - 1)
        draw.rectangle([top_left, bottom_right], fill='white')

    # Save the image with zero-padded step number
    filename = os.path.join(folder, f"step_{step:05d}.png")
    image.save(filename)

def part1(data, seconds=100):
    for i in range(seconds):
        data = [tick(robot) for robot in data]

    q1, q2, q3, q4 = count_quadrants(data)
    return q1 * q2 * q3 * q4
    

def part2(data, width=101, height=103, max_seconds=10000, folder="pictures", scale=5):
    for second in range(max_seconds):
        save_floor_image(data, width, height, folder, second, scale)
        
        data = [tick(robot, width, height) for robot in data]
        
        if (second + 1) % 1000 == 0:
            print(f"Simulated {second + 1} seconds...")
    return None

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
