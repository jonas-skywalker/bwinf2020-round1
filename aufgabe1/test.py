def complete2(_riddle, _words):
    punctuations = list()
    riddle = str()
    for i, val in enumerate(_riddle):
        if val in "!?.,;":
            punctuations.append((i, val))
        else:
            riddle += val

    riddle = riddle.split()

    print(riddle)

    solved = solve(riddle, _words)
    solved = " ".join(solved)

    for (key, val) in punctuations:
        solved = solved[:key] + val + solved[key:]

    return solved


def solve2(riddle, words):
    if len(riddle) == 0:
        return words
    for blank in riddle:
        possible = find_possible(blank, words)
        if possible:
            for word in possible:
                new_words = words[:]
                new_riddle = riddle[:]
                new_riddle[0] = word
                new_words.remove(word)
                solved_riddle = new_riddle[:1] + solve2(new_riddle[1:], new_words)
                return solved_riddle


def solve(riddle, words):
    print(riddle, words)
    if len(riddle) == 1:
        print(words)
        riddle[0] = words[0]
        return riddle
    else:
        possible = find_possible(riddle[0], words)
        if len(possible) == 0:
            print("No possible")
            return []
        for word in possible:
            new_words = words
            new_words.remove(word)
            new_solved = solve(riddle[1:], new_words)
            print("new", new_solved)
            if new_solved is []:
                break
            solution = [word] + new_solved
            if len(solution) > 1:
                return solution