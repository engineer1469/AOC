import time

def digest():
    with open('2025/6/input.txt', 'r') as f:
        lines = f.read().splitlines()

    data_lines = lines[:4]
    data = [[int(x) for x in line.split()] for line in data_lines]

    ops_line = lines[4]
    ops = ops_line.split()

    return data, ops  # data: List[List[int]], ops: List[str]


def part1(data, ops):
    rows = len(data)
    total = 0
    for col_idx, op in enumerate(ops):
        column_values = [data[row_idx][col_idx] for row_idx in range(rows)]
        if op == '+':
            total += sum(column_values)
        elif op == '*':
            prod = 1
            for v in column_values:
                prod *= v
            total += prod

    return total


def load_raw():
    with open("2025/6/input.txt") as f:
        lines = f.read().splitlines()
    grid = lines[:-1]
    op_row = lines[-1]
    return grid, op_row


def part2():
    grid, op_row = load_raw()
    H = len(grid)      # 4 digit rows
    W = len(op_row)    # width in characters

    def is_sep(col):
        # column of all spaces
        return all(grid[r][col] == " " for r in range(H)) and op_row[col] == " "

    # group columns into blocks (one block = one problem)
    problems = []
    block = []
    for c in range(W):
        if is_sep(c):
            if block:
                problems.append(block)
                block = []
        else:
            block.append(c)
    if block:
        problems.append(block)

    total = 0

    for block in problems:
        # find the single operator in this block
        ops_in_block = [op_row[c] for c in block if op_row[c] in "+*"]
        op = ops_in_block[0]

        digit_cols = [c for c in block if any(grid[r][c].isdigit() for r in range(H))]

        # read right-to-left
        digit_cols.reverse()

        nums = []
        for c in digit_cols:
            col_chars = [grid[r][c] for r in range(H)]
            s = "".join(col_chars)
            s = "".join(ch for ch in s if ch.isdigit())
            if not s:
                continue
            nums.append(int(s))

        if op == "+":
            total += sum(nums)
        else:
            prod = 1
            for v in nums:
                prod *= v
            total += prod

    return total


def main():
    data, ops = digest()
    st = time.time()
    result_part1 = part1(data, ops)
    print("part1:", result_part1)
    print("time:", time.time() - st)

    st = time.time()
    result_part2 = part2()
    print("part2:", result_part2)
    print("time:", time.time() - st)

if __name__ == '__main__':
    main()
