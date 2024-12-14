import time

def digest():
    data = []
    try:
        with open('2024/13/input.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: '2024/13/input.txt' not found.")
        return data

    for i in range(0, len(lines), 3):
        try:
            # Extract Button A coordinates
            a_parts = lines[i].split(':')[1].split(',')
            a_x = int(a_parts[0].split('+')[1])
            a_y = int(a_parts[1].split('+')[1])

            # Extract Button B coordinates
            b_parts = lines[i+1].split(':')[1].split(',')
            b_x = int(b_parts[0].split('+')[1])
            b_y = int(b_parts[1].split('+')[1])

            # Extract Prize coordinates
            prize_parts = lines[i+2].split(':')[1].split(',')
            prize_x = int(prize_parts[0].split('=')[1])
            prize_y = int(prize_parts[1].split('=')[1])

            data.append([(a_x, a_y), (b_x, b_y), (prize_x, prize_y)])
        except (IndexError, ValueError) as e:
            print(f"Skipping incomplete or malformed block starting at line {i+1}: {e}")

    return data  # list[list[(x, y), (x, y), (x, y)], ...]

def min_tokens_to_reach_target(v1, v2, p, max_presses=100):
    x1, y1 = v1
    x2, y2 = v2
    px, py = p

    min_tokens = None

    # Calculate the maximum possible presses for button B based on the X-axis
    max_b = min(px // x2, max_presses) if x2 != 0 else max_presses

    for b in range(0, max_b + 1):
        remainder_x = px - b * x2
        if remainder_x < 0:
            continue
        if x1 == 0:
            if remainder_x != 0:
                continue
            a = 0
        else:
            if remainder_x % x1 != 0:
                continue
            a = remainder_x // x1
            if a > max_presses:
                continue

        if y1 * a + y2 * b == py:
            tokens = 3 * a + b

            if (min_tokens is None) or (tokens < min_tokens):
                min_tokens = tokens
                if tokens == b:
                    break  # Early exit if minimal possible tokens are found

    return min_tokens

def min_tokens_to_reach_target_large(v1, v2, p):
    x1, y1 = v1
    x2, y2 = v2
    px, py = p

    denominator = y2 * x1 - y1 * x2
    numerator_b = py * x1 - px * y1

    if numerator_b % denominator != 0:
        return None

    b = numerator_b // denominator

    numerator_a = px - b * x2
    if numerator_a % x1 != 0:
        return None
    a = numerator_a // x1

    tokens = 3 * a + b
    return tokens

def part1(data):
    tokens_spent = 0
    for machine in data:
        a, b, p = machine
        tokens = min_tokens_to_reach_target(a, b, p)
        if tokens is not None:
            tokens_spent += tokens
    return tokens_spent

def part2(data):
    tokens_spent = 0
    adjustment = 10_000_000_000_000

    for machine in data:
        a, b, p = machine
        # Adjust prize coordinates
        adjusted_p = (p[0] + adjustment, p[1] + adjustment)
        tokens = min_tokens_to_reach_target_large(a, b, adjusted_p)
        if tokens is not None:
            tokens_spent += tokens
    return tokens_spent

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
