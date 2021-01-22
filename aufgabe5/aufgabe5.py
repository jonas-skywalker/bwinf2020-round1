import itertools
import math


def gen_adjazenz(data):
    adjazenz = dict()
    nodes = list(data.keys()) + [i * 10 for i in data.keys()]
    for key in nodes:
        adjazenz[key] = dict()
        for k in nodes:
            if k is not key:
                adjazenz[key][k] = 4
    for key, value in data.items():
        for v in value:
            if v is key:
                adjazenz[key * 10][v] = value.index(v) + 1
                adjazenz[key][v * 10] = value.index(v) + 1
            else:
                adjazenz[key][v] = value.index(v) + 1
                adjazenz[key][v * 10] = value.index(v) + 1
    return adjazenz


def shortest_path(adjazenz):
    visited = set()
    nodes_to_visit = set(adjazenz.keys())
    N = len(adjazenz.keys())
    distance_to_node = dict()
    for key in adjazenz.keys():
        distance_to_node[key] = math.inf
    distance_to_node[1] = 0
    paths = list()

    while nodes_to_visit:
        current_node = min(nodes_to_visit, key=lambda x: distance_to_node[x])
        for neighbour, cost_neighbour in adjazenz[current_node]:
            if neighbour in nodes_to_visit:
                cost = distance_to_node[current_node] + cost_neighbour
                if cost < distance_to_node[neighbour]:
                    distance_to_node[neighbour] = cost


class SpecialDict:
    def __init__(self, d):
        self.d = d

    def __sub__(self, other):
        result = dict()
        for self_k, self_v in self.d.items():
            if isinstance(self_v, list):
                self_value = self_v[0]
            else:
                self_value = self_v
            duplicate = False
            for other_k, other_v in other.d.items():
                if isinstance(other_v, list):
                    other_value = other_v[0]
                else:
                    other_value = other_v
                if self_k is other_k and self_value is other_value:
                    duplicate = True
            if not duplicate:
                if isinstance(self_v, list):
                    element = list(self_v)
                    for value in other.d.values():
                        if value in element:
                            del element[element.index(value)]
                else:
                    element = self_v
                result[self_k] = element
        return result

    def items(self):
        return self.d.items()

    def keys(self):
        return self.d.keys()

    def values(self):
        return self.d.values()


def sichere_wünsche(wünsche):
    sicher = dict()
    occurances = dict()
    for key in wünsche.keys():
        occurances[key] = 0
    for key, value in wünsche.items():
        occurances[value[0]] += 1
    for key, value in occurances.items():
        if value is 1:
            for k, v in wünsche.items():
                if wünsche[k][0] == key:
                    sicher[k] = wünsche[k][0]
    return sicher


def ret_verbelibende_geschenke(wünsche, sicher):
    total = len(wünsche)
    result = [i for i in range(1, total + 1)]
    for value in sicher.values():
        del result[result.index(value)]
    return result


def verteilung(wünsche):
    # alle ersten wünsche die erfüllt werden können
    sicher = sichere_wünsche(wünsche)
    print("Sicher sind", len(sicher), "Elemente:", sicher)
    verbleibend = SpecialDict(wünsche) - SpecialDict(sicher)
    print("Es verbleiben: ", verbleibend)
    verbleibende_geschenke = ret_verbelibende_geschenke(wünsche, sicher)
    verbleibende_spieler = list(verbleibend.keys())
    print("Verbleibende Spieler:", verbleibende_spieler)
    print("Die verbleibenden Geschenke sind:", verbleibende_geschenke)
    verteilungen = itertools.permutations(verbleibende_geschenke)
    verteilungen_scores = list()
    best = [[], [0, 0, 0]]
    for v in verteilungen:
        score = [0, 0, 0]
        for i in range(len(v)):
            geschenk = v[i]
            spieler = verbleibende_spieler[i]
            wunsch = wünsche[spieler]
            if geschenk in wunsch:
                score[wunsch.index(geschenk)] += 1
        if best[1][0] < score[0]:
            best = [v, score]
        elif best[1][0] == score[0]:
            if best[1][1] < score[1]:
                best = [v, score]
            elif best[1][1] == score[1]:
                if best[1][2] < score[2]:
                    best = [v, score]
        # verteilungen_scores.append([v, score])
    """
    max_score = max(verteilungen_scores, key=lambda x: x[1][0])[1][0]
    max_verteilungen = [x for x in verteilungen_scores if x[1][0] == max_score]
    # print(max_score, max_verteilungen)

    max_score_zweite_wahl = max(max_verteilungen, key=lambda x: x[1][1])[1][1]
    max_verteilungen = [x for x in max_verteilungen if x[1][1] == max_score_zweite_wahl]
    # print(max_score_zweite_wahl, max_verteilungen)

    max_score_dritte_wahl = max(max_verteilungen, key=lambda x: x[1][2])[1][2]
    max_verteilungen = [x for x in max_verteilungen if x[1][2] == max_score_dritte_wahl]
    # print(max_score_dritte_wahl, max_verteilungen)
    final = max_verteilungen[0]
    print(final)
    """
    print(best)
    final = best
    for i in range(len(final[0])):
        sicher[verbleibende_spieler[i]] = final[0][i]
    return sicher


def verteilung2(wünsche):
    """
    TODO: implement that it is looking for all possible combinations of the number of wishes it can grant
    :param wünsche:
    :return:
    """
    # alle ersten wünsche die erfüllt werden können
    sicher = sichere_wünsche(wünsche)
    print("Sicher sind", len(sicher), "Elemente:", sicher)
    verbleibend = SpecialDict(wünsche) - SpecialDict(sicher)
    print("Es verbleiben: ", verbleibend)
    verbleibende_geschenke = ret_verbelibende_geschenke(wünsche, sicher)
    verbleibende_spieler = list(verbleibend.keys())
    print("Verbleibende Spieler:", verbleibende_spieler)
    print("Die verbleibenden Geschenke sind:", verbleibende_geschenke)
    # generiere höchst mögliche zahl an zu erfüllenden ersten wünschen
    random_wunsch = set()
    while verbleibend:
        n_possible = len(set([x[0] for x in verbleibend.values()]))
        # now there is more than one possibility to ditribute the maximum number of gifts
        whishes_granted = dict()
        for i in range(n_possible):
            for key, value in verbleibend.items():
                if value[0] not in whishes_granted.values():
                    sicher[key] = value[0]
                    whishes_granted[key] = value[0]

        for key in whishes_granted.keys():
            del verbleibend[key]
            for key_v, value in verbleibend.items():
                if whishes_granted[key] in value:
                    del verbleibend[key_v][value.index(whishes_granted[key])]
                if not value:
                    random_wunsch.add(key_v)

        for key in random_wunsch:
            try:
                del verbleibend[key]
            except KeyError:
                pass
    verbleibende_geschenke = ret_verbelibende_geschenke(wünsche, sicher)
    # print("Random verteilte Geschenke:", verbleibende_geschenke, len(verbleibende_geschenke), len(random_wunsch))
    for key in random_wunsch:
        geschenk = verbleibende_geschenke.pop()
        sicher[key] = geschenk
    return sicher, len(sicher)


def verteilung3(wünsche, available_gifts, index=0):
    if len(wünsche) is 1:
        sicher = dict()
        wunsch = wünsche.items()[0]
        if wunsch[1]:
            sicher[wunsch[0]] = wunsch[1][0]
        else:
            sicher[wunsch[0]] = available_gifts[0]
        return sicher

    sicher = sichere_wünsche(wünsche)
    verbleibend = SpecialDict(wünsche) - SpecialDict(sicher)
    verbleibende_geschenke = ret_verbelibende_geschenke(wünsche, sicher)
    verbleibende_spieler = list(verbleibend.keys())
    possible = dict((i, []) for i in set([x[0] for x in verbleibend.values()]))
    for key, value in verbleibend.items():
        wish = value[0]
        if wish in possible.keys():
            possible[wish].append(key)
    n_possible = len(possible)
    print(possible, verbleibend)
    possible_vals = list(possible.values())
    combinations = [[x] for x in possible_vals.pop(0)]
    # find the possible ways to grant n_possible wishes

    for value in possible_vals:
        new_combinations = list()
        for comb in combinations:
            for val in value:
                new_combinations.append(comb + [val])
        combinations = list(new_combinations)

    print(combinations)


def score(verteilung, wünsche):
    scores = [0, 0, 0]
    for player, present in verteilung.items():
        player_wünsche = wünsche[player]
        if present in player_wünsche:
            scores[player_wünsche.index(present)] += 1
    return scores


if __name__ == '__main__':
    with open("../bwinf39-runde1/a5-Wichteln/beispieldaten/wichteln1.txt") as infile:
        n_players = int(infile.readline())
        data = dict()
        for i in range(1, n_players + 1):
            line = infile.readline()
            data[i] = [int(x) for x in line.split()]

    print(data)
    print(gen_adjazenz(data))
    # v = verteilung2(data)
    # print(dict(sorted(v[0].items(), key=lambda x: x[0])))
    # print(score(v[0], data))
    # print("==================================")
    # v2 = verteilung(data)
    # print(dict(sorted(v2.items(), key=lambda x: x[0])), score(v2, data))
    # print(gen_adjazenz(data))
    # v = verteilung3(data, list(data.keys()))
