import random
from timeit import default_timer as timer
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib import style

# style.use('fivethirtyeight')

# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)


def score(verteilung, wünsche):
    scores = [0, 0, 0]
    for player, present in verteilung.items():
        player_wünsche = wünsche[player]
        if present in player_wünsche:
            scores[player_wünsche.index(present)] += 1
    return scores


def gen_adjazenz(data):
    adjazenz = dict()
    nodes = list(data.keys())
    for key in nodes:
        adjazenz[key] = dict()
        for k in nodes:
            adjazenz[key][k] = 4
    for key, value in data.items():
        for v in value:
            adjazenz[key][v] = value.index(v) + 1
    return adjazenz, nodes
    # print(adjazenz)
    # new_adjazenz = dict()
    # for key, value in adjazenz.items():
    #     for k, v in value.items():
    #         new_adjazenz[(key, k)] = v
    # return new_adjazenz, nodes


def gen_adjazenz_greedy(data, verbleibende_geschenke):
    adjazenz1 = dict()
    nodes1 = list(data.keys())
    adjazenz2 = dict()
    nodes2 = [str(i) for i in verbleibende_geschenke]

    for key in nodes1:
        adjazenz1[key] = dict()
        for k in nodes2:
            adjazenz1[key][k] = 4
    for key, value in data.items():
        for v in value:
            if v in verbleibende_geschenke:
                adjazenz1[key][str(v)] = value.index(v) + 1

    for key in nodes2:
        adjazenz2[key] = dict()
        for k in nodes1:
            adjazenz2[key][k] = 0
    adjazenz1.update(adjazenz2)
    return adjazenz1, nodes1, nodes2


def fitness_path(path, ordered_nodes, sicher, data):
    verteilung = dict()
    for i in range(len(path)):
        verteilung[ordered_nodes[i]] = path[i]
    # verteilung.update(sicher)
    path_score = score(verteilung, data)
    return 100 * path_score[0] + 10 * path_score[1] + path_score[2]


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


def greedy_pop(adjazenz, nodes1, nodes2, POP_SIZE=16):
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
        sorted_path = sorted([(path[i-1], path[i]) for i in range(1, len(path), 2)], key=lambda x: x[0])
        real_path = [int(x[1]) for x in sorted_path]
        # print(real_path)
        pop.append(real_path)
    return pop


if __name__ == '__main__':
    start_timer = timer()
    with open("../bwinf39-runde1/a5-Wichteln/beispieldaten/wichteln1.txt") as infile:
        n_players = int(infile.readline())
        data = dict()
        for i in range(1, n_players + 1):
            line = infile.readline()
            data[i] = [int(x) for x in line.split()]

    print(data)
    sicher = sichere_wünsche(data)
    print(len(sicher))
    verbleibend = SpecialDict(data) - SpecialDict(sicher)
    verbleibende_geschenke = ret_verbelibende_geschenke(data, sicher)
    verbleibende_spieler = list(verbleibend.keys())

    ITERATIONS = 10000
    POPULATION_SIZE = 8
    MUTPROP = 0.05

    # TODO: Return greedy population of adjazenz with nearest neighbour algorithm
    # print({key: val for (key, val) in data.items() if key in verbleibende_spieler})
    greedy_adj, nodes1, nodes2 = gen_adjazenz_greedy({key: val for (key, val) in data.items() if key in verbleibende_spieler}, verbleibende_geschenke)
    # print(greedy_adj)
    # print(nodes1, nodes2)

    pop = greedy_pop(greedy_adj, verbleibende_spieler, [str(x) for x in verbleibende_geschenke], POP_SIZE=POPULATION_SIZE)

    # ungreedy pop:
    # adjazenz, nodes = gen_adjazenz(verbleibend)
    # pop = [random.sample(verbleibende_geschenke, len(verbleibende_geschenke)) for i in range(POPULATION_SIZE)]

    fitness = list()
    # calculate fittness of all paths
    for path in pop:
        fit = fitness_path(path, verbleibende_spieler, sicher, data)
        fitness.append((path, fit))
    pop = list(fitness)
    scores = list()

    for i in range(ITERATIONS):
        if i % 1000 == 0:
            print("[Calculating]: {}%".format(i/ITERATIONS * 100))
        pop.sort(key=lambda x: x[1], reverse=True)
        # print overall score of fastest path
        beste_verteilung = dict()
        if i % 1000 == 0:
            for i in range(len(pop[0][0])):
                beste_verteilung[verbleibende_spieler[i]] = pop[0][0][i]
            beste_verteilung.update(sicher)
            current_best = score(beste_verteilung, data)
            print(current_best)
            scores.append(current_best)
        # Selektion, auswählen von der population mit höherer warscheinlichkeit die besseren
        # fitness_sum = sum([x[1] for x in pop])
        # print(fitness_sum)
        # selektion_pop = [(x[0], sum([y[1] for y in pop[:pop.index(x) + 1]])) for x in pop]
        parents = random.choices(pop, weights=tuple(x[1] for x in pop), k=2)
        # print(parents)

        # crossover mit der definierten regel (ich hoffe das ist richtig TODO: korrigieren wenn nicht)
        cross_index = random.randint(0, len(parents[0][0]) - 1)
        child1 = parents[0][0][:cross_index]
        child2 = parents[1][0][:cross_index]
        parent1 = list(parents[0][0])
        parent2 = list(parents[1][0])
        crossover_start = timer()
        """
        while len(child1) < len(parents[0][0]):
            n1 = parent2.pop(0)
            if n1 not in child1:
                child1.append(n1)

        while len(child2) < len(parents[0][0]):
            n2 = parent1.pop(0)
            if n2 not in child2:
                child2.append(n2)
        """
        # this can be even faster with another method and multithreading
        child1 = parents[0][0][:cross_index] + [x for x in parent2 if x not in child1]
        child2 = parents[1][0][:cross_index] + [x for x in parent1 if x not in child2]

        children = [child1, child2]
        for i in range(len(children)):
            r = random.uniform(0, 1)
            if r < MUTPROP:
                index1 = random.randint(0, len(parents[0][0]) - 1)
                index2 = random.randint(0, len(parents[0][0]) - 1)
                temp = int(children[i][index2])
                children[i][index2] = int(children[i][index1])
                children[i][index1] = temp

        for i in range(len(children)):
            if children[i] not in [x[0] for x in pop]:
                pop[-1 - i] = (children[i], fitness_path(children[i], verbleibende_spieler, sicher, data))

    beste_verteilung = dict()
    for i in range(len(pop[0][0])):
        beste_verteilung[verbleibende_spieler[i]] = pop[0][0][i]
    print(scores)
    beste_verteilung.update(sicher)
    print(score(beste_verteilung, data), beste_verteilung)
    print(timer() - start_timer)
    # print(sorted(beste_verteilung.values()))
    # print(len(set(beste_verteilung.values())) == len(beste_verteilung.values()))
    # plt.plot(scores)
    # plt.show()
