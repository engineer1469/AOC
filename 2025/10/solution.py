from collections import deque
import time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def list_to_mask(lst):
    mask = 0
    for i, v in enumerate(lst):
        if v:
            mask |= (1 << i)
    return mask

def button_to_mask(indices):
    mask = 0
    for i in indices:
        mask |= (1 << i)
    return mask


def digest():
    with open('2025/10/input.txt', 'r') as f:
        data = f.read().splitlines()
        data_out = []

        for line in data:
            diagram = []
            buttons = []
            joltage_requirements = []

            # wiring diagrams
            target, rest = line.split(']')
            target = target[1:]
            for char in target:
                if char == '#':
                    diagram.append(True)
                else:
                    diagram.append(False)

            # buttons
            rest = rest.strip()
            buttons, rest = rest.split(' {')
            buttons = buttons.split('(')
            buttons = [b.strip()[:-1] for b in buttons if b]
            buttons = [list(map(int, b.split(','))) for b in buttons]

            # joltage requirements
            rest = rest.strip()
            rest = rest[:-1]
            joltage_requirements = [int(j) for j in rest.split(',')]

            # convert diagram + buttons to bitmasks
            diagram_mask = list_to_mask(diagram)
            button_masks = [button_to_mask(b) for b in buttons]

            data_out.append([diagram_mask, button_masks, joltage_requirements])

    return data_out
        

def find_minimal_combination(diagram_mask, button_masks):
    q = deque()
    visited = set()
    dist = {}

    start = 0
    q.append(start)
    visited.add(start)
    dist[start] = 0

    while q:
        state = q.popleft()

        if state == diagram_mask:
            return dist[state]

        for mask in button_masks:
            nxt = state ^ mask
            if nxt not in visited:
                visited.add(nxt)
                dist[nxt] = dist[state] + 1
                q.append(nxt)

def min_presses_joltage(button_masks, target): #Thanks claude :(
    """
    Solve using Mixed Integer Linear Programming (MILP).
    
    We want to find non-negative integers x_i (button presses) that:
    - Minimize sum(x_i)
    - Subject to: for each counter j, sum of x_i where button i affects counter j = target[j]
    
    This is: A @ x = target, x >= 0, minimize sum(x)
    """
    n = len(target)  # number of counters
    m = len(button_masks)  # number of buttons
  
    # Build the constraint matrix A where A[j][i] = 1 if button i affects counter j
    A = np.zeros((n, m), dtype=np.float64)
    for i, mask in enumerate(button_masks):
        for j in range(n):
            if (mask >> j) & 1:
                A[j, i] = 1.0
    
    target_arr = np.array(target, dtype=np.float64)
    
    # Objective: minimize sum of all x_i (i.e., coefficient 1 for each variable)
    c = np.ones(m)
    
    # Constraints: A @ x == target (equality constraint)
    constraints = LinearConstraint(A, target_arr, target_arr)
    
    # Bounds: x_i >= 0 (no upper bound)
    bounds = Bounds(lb=0, ub=np.inf)
    
    # All variables are integers
    integrality = np.ones(m, dtype=int)  # 1 means integer
    
    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)
    
    if result.success:
        return int(round(result.fun))
    else:
        return None

def part1(data):
    presses_sum = 0
    for machine in data:
        diagram_mask, button_masks, _ = machine
        presses = find_minimal_combination(diagram_mask, button_masks)
        presses_sum += presses
    return presses_sum


def part2(data):
    presses_sum = 0
    for machine in data:
        _, button_masks, joltage_requirements = machine
        presses = min_presses_joltage(button_masks, joltage_requirements)
        presses_sum += presses
    return presses_sum


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
