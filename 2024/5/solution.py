def digestRules():
    #list of tuples
    #key has to come before value in the update list
    with open('2024/5/rules.txt') as f:
        rules = f.read().splitlines()

    rulesList = []
    for rule in rules:
        rule = rule.split('|')
        rulesList.append((int(rule[0]), int(rule[1])))

    return rulesList

def digestUpdates():
    #list of lists
    with open('2024/5/updates.txt') as f:
        updates = f.read().splitlines()

    updatesList = []
    for update in updates:
        update = update.split(',')
        update = [int(i) for i in update]
        updatesList.append(update)

    return updatesList

def checkRule(rules, update):
    for i in range(len(update)):
        values = [value for key, value in rules if key == update[i]]
        #check if one of the values has to come before update[i]
        for value in values:
            if value in update[:i]:
                return False
            
    return True

def fixUpdate(rules, update):
    #if 2 numbers break a rule, flip them
    for i in range(len(update)):
        values = [value for key, value in rules if key == update[i]]
        #check if one of the values has to come before update[i]
        for value in values:
            if value in update[:i]:
                update[i], update[update.index(value)] = update[update.index(value)], update[i]
                return update
            
    return update

def part1(rules, updates):
    correct = []
    total = 0
    for update in updates:
        if checkRule(rules, update):
            correct.append(update)

    for update in correct:
        #append middle integers from correct list to correctMiddles
        middleIndex = int((len(update) - 1)/2)
        middle = update[middleIndex]
        total += middle

    incorrect = [update for update in updates if update not in correct]
    return total, incorrect

def part2(rules, incorrect):
    for update in incorrect:
        fixUpdate(rules, update)

    total, incorrect = part1(rules, incorrect)
    if len(incorrect) == 0:
        return total
    else:
        return total+part2(rules, incorrect)

def main():
    rules = digestRules()
    updates = digestUpdates()
    sumMiddle1, incorrect = part1(rules, updates)
    print("part1: ", sumMiddle1)
    print("part2: ", part2(rules, incorrect))

if __name__ == '__main__':
    main()