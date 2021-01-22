import random


def gen_adjazenz_greedy(data, verbleibende_geschenke):
    """
    Generiert die Adjazenz um die gierigen Pfade durch den Wunschgraphen zu generieren
    :param data:
    :param verbleibende_geschenke:
    :return:
    """
    # die adjazenz wird zunächst auf zwei dicts aufgeteilt um es einfacher zu halten. In adjazenz1 werden die Gewichte
    # von den Spielern zu den Geschenken, in adjazenz2 die null-Gewichte von den Geschenken zu den Spielern gespeichert
    adjazenz1 = dict()
    # nodes 1 sind alle Spieler
    nodes1 = list(data.keys())
    adjazenz2 = dict()
    # nodes 2 sind die Geschenke jedoch als String abgespeichert, Die Zahlen sind also die Spieler, die Strings die
    # Geschenke
    nodes2 = [str(i) for i in verbleibende_geschenke]

    # für jeden Spieler wird eine Verbindung mit dem Wert vier zu jedem Geschenk initilalisiert
    for key in nodes1:
        adjazenz1[key] = dict()
        for k in nodes2:
            adjazenz1[key][k] = 4
    # es wird nun, wenn die
    for key, value in data.items():
        for v in value:
            if v in verbleibende_geschenke:
                adjazenz1[key][str(v)] = value.index(v) + 1

    for key in nodes2:
        adjazenz2[key] = dict()
        for k in nodes1:
            adjazenz2[key][k] = 0
    adjazenz1.update(adjazenz2)
    return adjazenz1


def fitness_path(path, players, data, n_players):
    """
    Fitnessfunktion der Verteilungen, danach wird entschieden, wie gut eine Verteilung ist
    :param path: Verteilungsliste
    :param ordered_nodes: Die Hilfsliste, falls die Indexe der verteilung nicht kontinuirlich und geordnet sind
    :param data: die Wunschliste
    :param n_players: Anzahl an Spielern
    :return:
    """
    verteilung = dict()
    for i in range(len(path)):
        verteilung[players[i]] = path[i]
    path_score = score(verteilung, data)
    return n_players * n_players * path_score[0] + n_players * path_score[1] + path_score[2]


def score(verteilung, wünsche):
    """
    Erzeugt ein Tripel von der Anzahl an ersten, zweiten und dritten Wünschen, die mit einer Verteilung erfüllt wurden.
    :param verteilung: Die Verteilung ist hier ein Dictionary
    :param wünsche:
    :return:
    """
    scores = [0, 0, 0]
    for player, present in verteilung.items():
        player_wünsche = wünsche[player]
        if present in player_wünsche:
            scores[player_wünsche.index(present)] += 1
    return scores


def sichere_wünsche(wünsche):
    """
    Diese Methode nimmt ein Dictionary mit Spielern und ihren Wünschen an und berechnet, welche Spieler als einzige
    einen Geschenk möchten, welcher also kein anderer Spieler als erstes möchte.
    :param wünsche:
    :return:
    """
    # die Wünsche werden für später wieder in derselben Struktur abgespeichert
    sicher = dict()
    # occurrences enthält wür jedes Geschenk die Anzahl, wie oft es sich jemand als ersten Wunsch wünscht
    occurrences = dict()
    for key in wünsche.keys():
        occurrences[key] = 0
    for key, value in wünsche.items():
        occurrences[value[0]] += 1
    # Wenn also nur ein Spieler es als ersten Wunsch möchte, kann man diesem Spieler das Geschenk geben
    for key, value in occurrences.items():
        if value is 1:
            # finde heraus, wer das Geschenk wollte
            for k, v in wünsche.items():
                if wünsche[k][0] == key:
                    sicher[k] = wünsche[k][0]
    return sicher


def greedy_pop(adjazenz, nodes1, nodes2, POP_SIZE=16):
    """
    Generiert eine Population von gierigen Pfaden durch eine gegebene Adjazenz
    :param adjazenz:
    :param nodes1: Spielerknoten als Integerwerte
    :param nodes2: Geschenkknoten als Stringwerte
    :param POP_SIZE:
    :return:
    """
    pop = list()
    for i in range(POP_SIZE):
        path = list()
        current = random.choice(nodes1)
        path.append(current)
        to_visit = set(nodes1)
        to_visit.update(set(nodes2))
        to_visit.remove(current)
        while to_visit:
            neighbours = sorted(adjazenz[current].items(), key=lambda x: x[1])
            for i in range(len(neighbours)):
                if neighbours[i][0] in to_visit:
                    next = neighbours[i]
                    path.append(next[0])
                    current = next[0]
                    to_visit.remove(next[0])
                    break
        # convert path to normal representation
        # print(path)
        sorted_path = sorted([(path[i - 1], path[i]) for i in range(1, len(path), 2)], key=lambda x: x[0])
        real_path = [int(x[1]) for x in sorted_path]
        # print(real_path)
        pop.append(real_path)
    return pop


def genetic_algorithm(iterations, pop_size, mut, file):
    with open("../bwinf39-runde1/a5-Wichteln/beispieldaten/wichteln" + str(file) + ".txt") as infile:
        n_players = int(infile.readline())
        data = dict()
        for i in range(1, n_players + 1):
            line = infile.readline()
            data[i] = [int(x) for x in line.split()]

    print(data)
    sicher = sichere_wünsche(data)
    sichere_geschenke = [x[0] for x in sicher.values()]
    sichere_spieler = list(sicher.keys())
    print("Es gibt {} triviale Wünsche, die direkt erfüllt werden.".format(len(sicher)))
    # verbleibend ist auch ein Wunschdataobjekt, welches nur noch die Keys der Spieler enthält, die noch keinen Wunsch
    # erfüllt bekommen haben
    verbleibende_geschenke = [i for i in range(1, n_players + 1) if i not in sichere_geschenke]
    verbleibende_spieler = [i for i in range(1, n_players + 1) if i not in sichere_spieler]

    ITERATIONS = iterations
    POPULATION_SIZE = pop_size
    MUTPROP = mut

    greedy_adj = gen_adjazenz_greedy(
        {key: val for (key, val) in data.items() if key in verbleibende_spieler}, verbleibende_geschenke)
    pop = greedy_pop(greedy_adj, verbleibende_spieler, [str(x) for x in verbleibende_geschenke],
                     POP_SIZE=POPULATION_SIZE)

    fitness = list()
    # calculate fittness of all paths
    for path in pop:
        fit = fitness_path(path, verbleibende_spieler, data, n_players)
        fitness.append((path, fit))
    pop = list(fitness)

    for i in range(ITERATIONS):
        pop.sort(key=lambda x: x[1], reverse=True)
        # Selektion, auswählen von der population mit höherer warscheinlichkeit die besseren
        parents = random.choices(pop, weights=tuple(x[1] for x in pop), k=2)

        cross_index = random.randint(0, len(parents[0][0]) - 1)
        parent1 = list(parents[0][0])
        parent2 = list(parents[1][0])
        child1 = parent1[:cross_index]
        child2 = parent2[:cross_index]
        child1 += [x for x in parent2 if x not in child1]
        child2 += [x for x in parent1 if x not in child2]

        children = [child1, child2]

        for i in range(len(children)):
            r = random.uniform(0, 1)
            # Mutation öfter, wenn die Spieleranzahl länger ist, da nur eine Veränderung von 1000 wenig bringt
            if r < MUTPROP:
                for _ in range(int(n_players / 10)):
                    index1 = random.randint(0, len(parents[0][0]) - 1)
                    index2 = random.randint(0, len(parents[0][0]) - 1)
                    temp = int(children[i][index2])
                    children[i][index2] = int(children[i][index1])
                    children[i][index1] = temp

        for i in range(len(children)):
            if children[i] not in [x[0] for x in pop]:
                pop[-1 - i] = (children[i], fitness_path(children[i], verbleibende_spieler, data, n_players))

    beste_verteilung = dict()
    best_specimen = max(pop, key=lambda x: x[1])
    for i in range(len(best_specimen[0])):
        beste_verteilung[verbleibende_spieler[i]] = best_specimen[0][i]
    beste_verteilung.update(sicher)
    print(score(beste_verteilung, data), beste_verteilung)


if __name__ == '__main__':
    genetic_algorithm(100000000, 16, 0.5, 7)
