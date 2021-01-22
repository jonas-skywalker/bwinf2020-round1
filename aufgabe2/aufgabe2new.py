nachbarn_rules = [[],
                  [],
                  [((0, 2), (2, 0)), ((1, 1), (2, 1))],
                  [((3, 0), (2, 2))],
                  [],
                  [((5, 0), (1, 2)), ((5, 1), (4, 1))],
                  [((6, 0), (5, 2))],
                  [((7, 1), (6, 1)), ((7, 0), (3, 2))],
                  [((8, 0), (7, 2))]]


def rotated(l, ind=1):
    return l[ind:] + l[:ind]


def check_recent(path):
    tile_to_check = len(path) - 1
    score = [0]  # natürlich kann man nicht einfach alles aufeinander addieren,
    # da sich auch fehlstellungen rauskkürzen können: 0 = 4-3 + 3-4
    for item in path[:-1]:
        # hier sollte ein Counter benutzt werden um zu wissen ob es das Teil nicht vielleicht doppelt gibt
        if item in [path[-1], rotated(path[-1]), rotated(path[-1], ind=2)]:
            return False
    for rule in nachbarn_rules[tile_to_check]:
        (teil1, figur1), (teil2, figur2) = rule
        score.append(path[teil1][figur1] + path[teil2][figur2])
    if set(score) == {0}:
        return True
    else:
        return False


def solve(n_figuren, n_teile, teile):
    """
    Die Funktion solve gibt alle möglichen Lösungen einer Puzzledatei an. Das Puzzle wird als gerichteter Graph
    interpretiert. Die Lösung ist also ein möglicher Pfad durch den Graphen. Ein Pfad erhält genau alle neun Teile
    des Puzzles hintereinander sodass aus einer Liste von neun Teilen eine Pyramide gelesen von oben nach unten und
    links nach rechts entsteht (Siehe Grafik in der Erklärung der Bearbeitung).
    :param n_figuren:
    :param n_teile:
    :param teile:
    :return:
    """
    # paths enthält alle möglichen Pfade wie man die Teile aneinander Ordnen kann
    paths = list()
    # es wird nun zunächst eine Liste erstellt mit allen 27 möglichen Teilen, da man jedes Teil gegen und im
    # Uhrzeigersinn drehen kann. Es wird auch für jedes Teil einen möglichen Pfad angelegt, da man das Puzzle mit jedem
    # der Teile in der ersten Position anfangen kann.
    alle_teile = list()
    for teil in teile:
        paths.append([teil])
        paths.append([rotated(teil)])
        paths.append([rotated(teil, ind=2)])
        alle_teile.append(teil)
        alle_teile.append(rotated(teil))
        alle_teile.append(rotated(teil, ind=2))

    # Es existieren gerade also 27 Pfade mit der Länge eins. Mit jeder Iteration wird diese Zahl erhöht bis die länge 9
    # erreicht ist, also alle Teile in dem Pfad benutzt wurden.
    length = 1
    # Es werden nun in der folgenden while-Schleife alle möglichen weiteren Pfade mit bestimmten Kriterien generiert.
    # Wenn es nach einer bestimmen Iteration keine Pfade mehr gibt, bedeutet es, dass keine mögliche Lösung exisitiert,
    # also eine leere Liste ausgegeben wird.
    while paths:
        if length == 9:
            break
        # Die neu generierten Pfade werden in der new_paths Variable festgehalten
        new_paths = list()
        for i in range(len(paths)):
            # finde alle Teile die noch nicht in diesem Pfad besucht wurden
            possible = [x for x in alle_teile if x not in paths[i]]
            # Die neuen Teile werden an die jeweiligen Pfade angehängt
            for new in possible:
                new_paths.append(paths[i] + [new])
        # bis jetzt enthält die new_paths variable alle naiven Pfade. Jedoch kann es sein, dass das Teil , welches
        # angehängt wurde, schon in einer rotierten Weise im bsiherigen Pfad exisitert. Auch muss überprüft werden, ob
        # die Figuren des neu angehängten Teiles zu den Figuren der bisherigen Teile passen.
        paths = list()
        for i in range(len(new_paths)):
            # check_recent überprüft diese Kriterien und es wird der Pfad angehängt
            if check_recent(new_paths[i]):
                paths.append(new_paths[i])
        # Die Länge aller Pfade beträgt nun eins mehr, es ist jedoch möglich, dass ab hier keine Pfade mehr exisiteren,
        # weil das Problem nicht lösbar ist.
        length += 1
        # print(len(paths), length)

    print("Die Lösungen sind:", paths)
    print("Es exisitieren {} einzigartige Lösungen.".format(int(len(paths)/3)))


if __name__ == '__main__':
    # Einlesen der Datei des Puzzles
    with open("../bwinf39-runde1/a2-Dreieckspuzzle/beispieldaten/puzzle2.txt") as infile:
        n_figuren = int(infile.readline())
        n_teile = int(infile.readline())
        teile = list()
        for i in range(n_teile):
            teil = [int(x) for x in infile.readline().split()]
            teile.append(teil)

    print(n_figuren, n_teile, teile)
    solve(n_figuren, n_teile, teile)
