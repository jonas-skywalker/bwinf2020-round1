import itertools


nachbarn = [((0, 2), (2, 0)),
            ((1, 1), (2, 1)), ((1, 2), (5, 0)),
            ((2, 2), (3, 0)),
            ((3, 2), (7, 0)),
            ((4, 1), (5, 1)),
            ((5, 2), (6, 0)),
            ((6, 1), (7, 1)),
            ((7, 2), (8, 0))]


beispiel = [[1, -2, -3], [-2, 3, 2], [3, -3, 1], [-1, 2, -3], [-2, -1, 1], [-2, 1, 1], [-1, 2, -2], [3, -2, -1], [1, -2, -2]]


def rotated(l, i=1):
    return l[i:] + l[:i]


def check(teil):
    score = 0
    index = 0
    while score == 0:
        if index == len(nachbarn):
            return True, index
        (teil1, figur1), (teil2, figur2) = nachbarn[index]
        score += teil[teil1][figur1] + teil[teil2][figur2]
        index += 1
    return False, index


if __name__ == '__main__':
    with open("./puzzle3.txt") as infile:
        print("aufgabe2, 3")
        n_figuren = int(infile.readline())
        n_teile = int(infile.readline())
        teile = list()
        for i in range(n_teile):
            teil = [int(x) for x in infile.readline().split()]
            teile.append(teil)

    print(n_figuren, n_teile, teile)
    solved = list()
    count = 0
    total = 362880
    for permutation in itertools.permutations(teile):
        rotations = list()
        for i in range(len(permutation)):
            rotations.append([permutation[i], rotated(permutation[i]), rotated(permutation[i], i=2)])
        combinations = [[x] for x in rotations.pop(0)]
        for value in rotations:
            new_combinations = list()
            for comb in combinations:
                for val in value:
                    new_combinations.append(comb + [val])
            combinations = list(new_combinations)
        for comb in combinations:
            valid, index = check(comb)
            if valid:
                print("SOLVED IT")
                solved = comb
                break
            else:
                if index < 2:
                    cut = index - 1
                else:
                    cut = index - 2
        if solved:
            break
        if (count % 100 == 0):
            print(count/total * 100)
        count += 1
    if solved:
        print("Solvable with:", solved)
    else:
        print("Unsolvable")
