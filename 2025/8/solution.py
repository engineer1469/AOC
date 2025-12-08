import time
from typing import TypedDict

# custom datatypes for junction boxes
class JunctionBox(TypedDict):
    id: int
    x: int
    y: int
    z: int
    connections: list[int]
    closest_box: int
    cb_distance: float

def digest():
    with open('2025/8/input.txt', 'r') as f:
        data = f.read().splitlines()
        for i in range(len(data)): #x,y,z per line
            x, y, z = map(int, data[i].split(','))
            data[i] = JunctionBox(
                id=i,
                x=x,
                y=y,
                z=z,
                connections=[],
                closest_box=-1,
                cb_distance=-1.0
            )
    return data #List[JunctionBox]

def calculate_distance_squared(box: JunctionBox, box2: JunctionBox):
    dx = box['x'] - box2['x']
    dy = box['y'] - box2['y']
    dz = box['z'] - box2['z']
    return dx*dx + dy*dy + dz*dz

def calculate_closest(box: JunctionBox, data):
    min_distance = float('inf')
    closest_id = -1
    
    for comparison_box in data:
        if comparison_box['id'] == box['id']:
            continue  # Skip comparing box to itself
        
        dist_squared = calculate_distance_squared(box, comparison_box)
        if dist_squared < min_distance:
            min_distance = dist_squared
            closest_id = comparison_box['id']
    
    box['closest_box'] = closest_id
    box['cb_distance'] = min_distance ** 0.5

def connect_boxes(box: JunctionBox, box2: JunctionBox, circuits):
    """Returns True if a new connection was made (boxes were in different circuits)"""
    # Check if a box is in a circuit already
    box_circuit = None
    box2_circuit = None
    for circuit in circuits:
        if box['id'] in circuit:
            box_circuit = circuit
        if box2['id'] in circuit:
            box2_circuit = circuit

    if box_circuit and box2_circuit:
        if box_circuit == box2_circuit:
            # Already in same circuit
            return False
        # Merge circuits
        box_circuit.update(box2_circuit)
        circuits.remove(box2_circuit)

    elif box_circuit:
        box_circuit.add(box2['id'])

    elif box2_circuit:
        box2_circuit.add(box['id'])

    else:
        circuits.append({box['id'], box2['id']})

    box['connections'].append(box2['id'])
    box2['connections'].append(box['id'])
    return True

def part1(data):
    circuits = []  # List[set[int]]
    
    all_pairs = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            dist_sq = calculate_distance_squared(data[i], data[j])
            all_pairs.append((dist_sq, i, j))

    all_pairs.sort()

    for dist_sq, i, j in all_pairs[:1000]:
        connect_boxes(data[i], data[j], circuits)
    
    largest_circuits = sorted(circuits, key=len, reverse=True)[:3]
    product = 1
    for circuit in largest_circuits:
        product *= len(circuit)

    return product


def part2(data):
    circuits = []  # List[set[int]]
    
    # Calculate ALL pairwise distances
    all_pairs = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            dist_sq = calculate_distance_squared(data[i], data[j])
            all_pairs.append((dist_sq, i, j))
    
    all_pairs.sort()
    
    # Connect pairs until all boxes are in one circuit
    n_boxes = len(data)
    for dist_sq, i, j in all_pairs:
        connected = connect_boxes(data[i], data[j], circuits)
        
        if connected and len(circuits) == 1 and len(circuits[0]) == n_boxes:
            # This was the final connection
            return data[i]['x'] * data[j]['x']
    
    return None

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
