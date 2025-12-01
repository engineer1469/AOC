import re

def digest():
    with open('2024/3/input.txt') as f:
        raw_data = f.read()
        pattern = r"mul\((\d+),(\d+)\)"
        return re.findall(pattern, raw_data)
    
def digest2():
    with open('3/input.txt') as f:
        raw_data = f.read()
        #pattern that matches 'mul', 'do', 'don't', or any other character
        pattern = r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)"
        tokens = re.finditer(pattern, raw_data)
        
        enabled = True
        data = []
        
        for m in tokens:
            token = m.group(0)
            if token == "do()":
                enabled = True
            elif token == "don't()":
                enabled = False
            elif token.startswith("mul"):
                if enabled:
                    a, b = m.group(1), m.group(2)
                    data.append((a, b))
            # Ignore any other text
        return data
    
def solve(data):
    total = 0
    for a, b in data:
        total += int(a) * int(b)
    return total

def main():
    data = digest()
    result = solve(data)
    print("part one: ",result)
    data = digest2()
    result = solve(data)
    print("part two: ",result)

if __name__ == '__main__':
    main()