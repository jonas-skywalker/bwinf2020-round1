import random
import math


def match(player1, player2, welcher=False):
    """
    Die Match funktion zwischen zwei Spielern simuliert den in der Aufgabe beschriebenen Urnenvorgang, gibt den Hinweis
    welcher Spieler gewonnen hat wenn wich True ist
    :param welcher:
    :param player1: Spielstärke des ersten Spielers
    :param player2: Spielstärke des zweiten Spielers
    :return: die Spielstärke des Gewinners
    """
    # es wird eine Zufallszahl zwischen 0 und 1 generiert
    r = random.random()
    sum = player1 + player2
    # Das Teilen der Spielstärke durch die Summe der Spielstärken normiert die Spielstärke auf einen Bereich zwischen
    # 0 und 1. Wenn die Zufallszahl im Bereich 0 bis zur normierten Spielstärke liegt, gewinnt Spieler eins, ansonsten
    # spieler zwei
    if r < player1/sum:
        if welcher:
            return player1, True
        else:
            return player1
    else:
        if welcher:
            return player2, False
        else:
            return player2


def ko(spielstärken):
    """
    Funktion zur Berechnung er Ko-Variante
    :param spielstärken: Liste der Spielstärken als Integer
    :return: Wahrheitswert ob bester Spieler der Gewinner ist (boolean), Gewinner (int), bester Spieler (int)
    """
    # ermittlung des besten Spielers mit der höchsten Spielstärke
    best_player = max(spielstärken)
    # Für das Ko system wird eine Zweierpotenz an Spielern benötigt. math.log(len(spielstärken), 2)) ist die Anzahl an
    # Runden des ko systems. Wenn ich also 16 spieler habe, benötige ich 4 Runden: 16 - 8 - 4 - 2 - 1
    for i in range(int(math.log(len(spielstärken), 2))):
        # spielstärken der nächsten Runde
        new_spielstärken = list()
        # jeweils die zwei nebeneinander machen ein Match, der der gewinnt wird in die nächste Runde aufgenommen
        for match_index in range(0, len(spielstärken) - 1, 2):
            new_spielstärken.append(match(spielstärken[match_index], spielstärken[match_index + 1]))
        # die neuen Spielstärken werden zu den Spielstärken der nächsten Runde
        spielstärken = new_spielstärken
    # jetzt ist nur noch eine Spielstärke vorhanden, der Gewinner des Turniers
    return spielstärken[0] is best_player, spielstärken[0], best_player


def ko_x5(spielstärken):
    """
    Selbe Funktion wie ko(), jedoch wird das Ko-Match fünf mal ausgeführt
    :param spielstärken:
    :return: Wahrheitswert ob bester Spieler der Gewinner ist (boolean), Gewinner (int), bester Spieler (int)
    """
    best_player = max(spielstärken)
    for i in range(int(math.log(len(spielstärken), 2))):
        new_spielstärken = list()
        for match_index in range(0, len(spielstärken) - 1, 2):
            # Winners behält die bisherigen Gewinner, es wird also erst 5 mal gespielt und dann die häufiger vorkommende
            # Spielstärke in der winners Liste als Gewinner erklärt
            winners = list()
            for j in range(5):
                winners.append(match(spielstärken[match_index], spielstärken[match_index + 1]))
            # das Set enthält die beiden Spielstärken. Es wird mit der max Funktion ermittelt welche der Beiden öfter
            # vorkommen,der key ist dabei gegeben durch List.count(element)
            new_spielstärken.append(max(set(winners), key=winners.count))
        spielstärken = new_spielstärken
    return spielstärken[0] is best_player, spielstärken[0], best_player


def liga(spielstärken):
    """
    Funktion um das Ligasystem zu simulieren
    :param spielstärken: Liste von Spielstärken
    :return: Wahrheitswert ob bester Spieler der Gewinner ist (boolean), Gewinner (int), bester Spieler (int)
    """
    best_player = max(spielstärken)

    # Die total liste enthält den Wert wie oft ein bestimmter Spieler des Indexes i mit der Spielstärke gewonnen
    # hat
    total = [0 for _ in range(len(spielstärken))]

    # Iteration sodass jeder gegen jeden einmal gespielt hat
    for i in range(len(spielstärken)):
        for j in range(i + 1, len(spielstärken)):
            # Wichtig, man benötigt hier die welcher variable falls die Spielstärken gleich sind
            winner, isplayer1 = match(spielstärken[i], spielstärken[j], welcher=True)
            if isplayer1:
                total[i] += 1
            else:
                total[j] += 1
    spielstärke_winner = spielstärken[total.index(max(total))]
    return spielstärke_winner is best_player, spielstärke_winner, best_player


if __name__ == '__main__':
    with open("../bwinf39-runde1/a3-Tobis-Turnier/beispieldaten/spielstaerken1.txt") as infile:
        spielstärken = infile.readlines()
        for i in range(len(spielstärken)):
            spielstärken[i] = int(spielstärken[i].strip("\n"))
        del spielstärken[0]
        count_best_player_won = 0
        repetitions = 100000
        for i in range(repetitions):
            best_player_won, winner, best_player = ko(spielstärken)
            if best_player_won:
                count_best_player_won += 1
        print("Prozentsatz(Ko): ", count_best_player_won/repetitions * 100)

        count_best_player_won = 0
        for i in range(repetitions):
            best_player_won, winner, best_player = ko_x5(spielstärken)
            if best_player_won:
                count_best_player_won += 1
        print("Prozentsatz(Kox5): ", count_best_player_won / repetitions * 100)

        count_best_player_won = 0
        for i in range(repetitions):
            best_player_won, winner, best_player = liga(spielstärken)
            if best_player_won:
                count_best_player_won += 1
        print("Prozentsatz(Liga): ", count_best_player_won / repetitions * 100)
