import time
import concurrent.futures

PROGRAM = [2,4,1,1,7,5,4,6,0,3,1,4,5,5,3,0]

def find_combo(operand, A, B, C):
    if operand in [0, 1, 2, 3]:
        return operand
    elif operand == 4:
        return A
    elif operand == 5:
        return B
    elif operand == 6:
        return C
    else:
        raise ValueError(f"Invalid operand: {operand}")

def adv(operand, A, B, C):
    A = A // (2 ** find_combo(operand, A, B, C))
    return A, B, C

def bxl(operand, A, B, C):
    B = B ^ operand
    return A, B, C

def bst(operand, A, B, C):
    B = find_combo(operand, A, B, C) % 8
    return A, B, C

def bxc(operand, A, B, C):
    B = B ^ C
    return A, B, C

def out(operand, A, B, C):
    return find_combo(operand, A, B, C) % 8

def bdv(operand, A, B, C):
    B = A // (2 ** find_combo(operand, A, B, C))
    return A, B, C

def cdv(operand, A, B, C):
    C = A // (2 ** find_combo(operand, A, B, C))
    return A, B, C

def part1(A, B, C, program):
    output = []
    i = 0
    while i < len(program):
        opcode = program[i]
        operand = program[i+1]

        if opcode == 0:
            A, B, C = adv(operand, A, B, C)
        elif opcode == 1:
            A, B, C = bxl(operand, A, B, C)
        elif opcode == 2:
            A, B, C = bst(operand, A, B, C)
        elif opcode == 3:  # jnz
            if A != 0:
                i = operand
                continue
        elif opcode == 4:
            A, B, C = bxc(operand, A, B, C)
        elif opcode == 5:
            output.append(out(operand, A, B, C))
        elif opcode == 6:
            A, B, C = bdv(operand, A, B, C)
        elif opcode == 7:
            A, B, C = cdv(operand, A, B, C)

        i += 2

    return output

def test_chunk(start, end):
    print(f"Testing chunk {start}-{end}")
    for i in range(start, end):
        A = i
        B = 0
        C = 0
        result = part1(A, B, C, PROGRAM)
        if result == PROGRAM:
            return i
    return None

def part2():
    chunk_size = 100000
    max_workers = 12  # adjust depending on your CPU
    start = 0
    
    # We'll keep a small number of chunks in flight at once
    # As soon as one finishes, if no result, we submit another
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        # pre-fill the pipeline
        for _ in range(max_workers):
            end = start + chunk_size
            fut = executor.submit(test_chunk, start, end)
            futures[fut] = (start, end)
            start = end

        while futures:
            done, _ = concurrent.futures.wait(futures.keys(), return_when=concurrent.futures.FIRST_COMPLETED)
            for fut in done:
                res = fut.result()
                if res is not None:
                    # Found the result, cancel remaining tasks
                    for f in futures:
                        f.cancel()
                    return res
                else:
                    # Not found in this chunk, submit another chunk
                    del futures[fut]
                    end = start + chunk_size
                    new_fut = executor.submit(test_chunk, start, end)
                    futures[new_fut] = (start, end)
                    start = end

def main():
    # Just test part1 for a known value
    st = time.time()
    result_part1 = part1(28066687, 0, 0, PROGRAM)
    print("part1:", result_part1)
    print("time:", time.time() - st, "seconds")

    # Now run part2 without a known max limit
    st = time.time()
    result_part2 = part2()
    print("\npart2:", result_part2)
    print("time:", time.time() - st, "seconds")

if __name__ == '__main__':
    main()
