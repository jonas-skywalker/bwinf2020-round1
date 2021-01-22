import itertools


nachbarn9 = [((0, 2), (2, 0)),
            ((1, 1), (2, 1)), ((1, 2), (5, 0)),
            ((2, 2), (3, 0)),
            ((3, 2), (7, 0)),
            ((4, 1), (5, 1)),
            ((5, 2), (6, 0)),
            ((6, 1), (7, 1)),
            ((7, 2), (8, 0))]

nachbarn3 = [((0, 2), (2, 0)), ((1, 1), (2, 1)), ((2, 2), (3, 0))]


beispiel = [[1, -2, -3], [-2, 3, 2], [3, -3, 1], [-1, 2, -3], [-2, -1, 1], [-2, 1, 1], [-1, 2, -2], [3, -2, -1], [1, -2, -2]]


def rotated(l, i=1):
    return l[i:] + l[:i]


def check(teil):
    score = 0
    index = 0
    while score == 0:
        if index == len(nachbarn3):
            return True, index
        (teil1, figur1), (teil2, figur2) = nachbarn3[index]
        score += teil[teil1][figur1] + teil[teil2][figur2]
        index += 1
    return False, index


if __name__ == '__main__':
    with open("../bwinf39-runde1/a2-Dreieckspuzzle/beispieldaten/puzzle2.txt") as infile:
        print("aufgabe2, 2")
        n_figuren = int(infile.readline())
        n_teile = int(infile.readline())
        teile = list()
        for i in range(n_teile):
            teil = [int(x) for x in infile.readline().split()]
            teile.append(teil)

    print(n_figuren, n_teile, teile)
    teile_ordered = sorted([sorted(x) for x in teile], key=lambda x: x[0])
    print(teile_ordered)
    solved = list()
    valids = list()
    count = 0
    total = 362880
    for permutation in itertools.permutations(teile, r=4):
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
                valids.append(comb)
        if count % 100 == 0:
            print(count / total * 100)
        count += 1
    print(len(valids))
    for element1 in valids:
        if solved:
            break
        turns1 = [element1, [rotated(element1[3]), rotated(element1[0]), rotated(element1[2], i=2), rotated(element1[1])],
                  [rotated(element1[1], i=2), rotated(element1[3], i=2), rotated(element1[2], i=1), rotated(element1[0], i=2)]]
        for element2 in valids:
            if solved:
                break
            turns2 = [element2, [rotated(element2[3]), rotated(element2[0]), rotated(element2[2], i=2), rotated(element2[1])],
                      [rotated(element2[1], i=2), rotated(element2[3], i=2), rotated(element2[2], i=1), rotated(element2[0], i=2)]]

            possible_matches = list()
            for turned1 in turns1:
                for turned2 in turns2:
                    if turned1[1] == turned2[0]:
                        possible_matches.append([turned1, turned2])
            if not possible_matches:
                break
            for element3 in valids:
                if solved:
                    break
                turns3 = [element3, [rotated(element3[3]), rotated(element3[0]), rotated(element3[2], i=2), rotated(element3[1])],
                          [rotated(element3[1], i=2), rotated(element3[3], i=2), rotated(element3[2], i=1), rotated(element3[0], i=2)]]

                for possible in possible_matches:
                    if solved:
                        break
                    for turned3 in turns3:
                        if turned3[0] == possible[0][3] and turned3[1] == possible[1][3]:
                            poss_solved = possible[0] + possible[1][1:] + turned3[2:]
                            # check if solved contains same tiles and is not using every tile only once
                            solved_ordered = sorted([sorted(x) for x in poss_solved], key=lambda x: x[0])
                            print(solved_ordered, teile_ordered)
                            if solved_ordered == teile_ordered:
                                print(solved_ordered, teile_ordered)
                                solved = poss_solved
                                break
    if solved:
        print("Solvable with: ", solved)
    else:
        print("Not solvable!")

