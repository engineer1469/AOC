def digest():
    with open('2024/1/input.txt', 'r') as f:
        l1 = []
        l2 = []
        for line in f:
            p1, p2 = line.strip().split('   ')
            l1.append(int(p1))
            l2.append(int(p2))
    return l1, l2

def distance(p1, p2):
    return abs(p1 - p2)

def calculateDistances(l1, l2):
    distances = []
    for i in range(len(l1)):
        p1 = l1[i]
        p2 = l2[i]
        distances.append(distance(p1, p2))
    return distances

def calculateSimilarities(l1, l2):
    similarities = []
    for p1 in l1:
        similarities.append(p1 * l2.count(p1))
    return similarities


def main():
    l1, l2 = digest()
    l1.sort()
    l2.sort()
    distances = calculateDistances(l1, l2)
    similarities = calculateSimilarities(l1, l2)

    print("distances: ",sum(distances))
    print("similarities: ",sum(similarities))

if __name__ == '__main__':
    main()