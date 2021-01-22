def score(verteilung, wünsche):
    scores = [0, 0, 0]
    for player, present in verteilung.items():
        player_wünsche = wünsche[player]
        if present in player_wünsche:
            scores[player_wünsche.index(present)] += 1
    return scores


def replace(l, vals):
    result = list(l)
    for i in range(len(l)):
        if l[i] in vals:
            result[i] = 0
    return result


if __name__ == '__main__':
    """
    GREEDY APPROACH
    """
    with open("../bwinf39-runde1/a5-Wichteln/beispieldaten/wichteln7.txt") as infile:
        n_players = int(infile.readline())
        data = dict()
        for i in range(1, n_players + 1):
            line = infile.readline()
            data[i] = [int(x) for x in line.split()]

    print(data, "\n")
    wünsche = dict(data)
    finished = dict()
    for _ in range(3):
        wishes = set([value[0] for (key, value) in data.items() if value[0] is not 0])
        solved = dict()
        while wishes:
            for key in data.keys():
                if data[key][0] in wishes:
                    solved[key] = data[key][0]
                    wishes.remove(data[key][0])
        finished.update(solved)
        [data.pop(key) for key in solved.keys()]
        data = {key: replace(data[key][1:], solved.values()) for key in data.keys()}
        print(data, solved)

    print(data)
    verbleibende_geschenke = [geschenk for geschenk in wünsche.keys() if geschenk not in finished.values()]
    print(verbleibende_geschenke)
    verbleibende_spieler = list(data.keys())
    for i in range(len(verbleibende_geschenke)):
        finished[verbleibende_spieler[i]] = verbleibende_geschenke[i]
    print(score(finished, wünsche), finished, len(finished))
