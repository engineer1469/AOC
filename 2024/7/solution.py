import time

def digest():
    with open('2024/7/input.txt') as f:
        lines = f.read().strip().splitlines()
        return [[int(value.rstrip(':')) for value in line.split()] for line in lines]

def boolean_enumerator(length):
    for i in range(2**length):
        bits = []
        n = i
        for _ in range(length):
            bits.append((n & 1) == 1)
            n >>= 1
        yield bits

def evaluate(equation, bools):
    if len(equation) < 2:
        return equation[0] if equation[0] == 0 else 0
    
    total = equation[1]
    for i, op in enumerate(bools):
        next_num = equation[i+2]
        if op:  # True means addition
            total += next_num
        else:   # False means multiplication
            total *= next_num

    return total if total == equation[0] else 0

def part1(data):
    total = 0
    for equation in data:
        length = len(equation) - 2
        found = False
        for bools in boolean_enumerator(length):
            if evaluate(equation, bools) == equation[0]:
                found = True
                break
        if found:
            total += equation[0]
    return total

def can_make_target_with_all_ops(nums, target):
    if len(nums) == 1:
        return nums[0] == target
    
    # Try each operator between nums[0] and nums[1]
    # 1) Addition
    add_result = [nums[0] + nums[1]] + nums[2:]
    if can_make_target_with_all_ops(add_result, target):
        return True

    # 2) Multiplication
    mul_result = [nums[0] * nums[1]] + nums[2:]
    if can_make_target_with_all_ops(mul_result, target):
        return True

    # 3) Concatenation (||)
    concat_num = int(str(nums[0]) + str(nums[1]))
    concat_result = [concat_num] + nums[2:]
    if can_make_target_with_all_ops(concat_result, target):
        return True

    return False

def part2(data):
    total = 0
    for equation in data:
        target = equation[0]
        nums = equation[1:]
        # Check if we can form the target using +, *, and ||
        if can_make_target_with_all_ops(nums, target):
            total += target
    return total

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
