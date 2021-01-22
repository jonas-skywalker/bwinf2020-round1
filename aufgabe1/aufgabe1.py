import codecs
from collections import Counter


"""
Rätsel  0 : 
_h __, _a_ __r ___e __b___!

Ausgefüllt:  oh je, was für eine arbeit! 


Rätsel  1 : 
_m ___a__ ____e __s ____e____ __________. D__ _a____ _i___ __u__ ____ ___e__ _n_ _u___ ____________ _l_ __h____ __ ___ _____h_ ________ _____e___.

Ausgefüllt:  Am Anfang wurde das Universum erschaffen. Das machte viele Leute sehr wütend und wurde allenthalben als Schritt in die falsche Richtung angesehen. 


Rätsel  2 : 
__s __e___ _a___ e____ _____n_ _u_ _________ ____m__ ________, _a__ _r s___ _n _____m ___t _u ____m ___________ ______e___ _______e__.

Ausgefüllt:  Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich in seinem Bett zu einem ungeheueren Ungeziefer verwandelt. 


Rätsel  3 : 
__________ __t d__ ____e_______ __n _e_ ______________ __________g, __e________, ___a________ _n_ ___r_______ __n ___o_________, _________ _e_ ______t______ ___a________ _i_ _______________.

Ausgefüllt:  Informatik ist die Wissenschaft von der systematischen Darstellung, Speicherung, Verarbeitung und Übertragung von Informationen, besonders der automatischen Verarbeitung mit Digitalrechnern. 


Rätsel  4 : 
__a _____n _______t _n _i___ _e_________ __s d__ _____e__ __d _i____ e__ __t___. _s _s_ __n_ ____e __n ______n ___e___, _i_ i_ _i_ ___h____ __________e __b_____ ___d__ s_____, _o __s_ s__ _i__ ___t___ _e________ _r_____. __________n _n_ _a_________ s____ e_____ _______b__ ___d ____n ______e___.

Ausgefüllt:  Opa Jürgen blättert in einer Zeitschrift aus der Apotheke und findet ein Rätsel. Es ist eine Liste von Wörtern gegeben, die in die richtige Reihenfolge gebracht werden sollen, so dass sie eine lustige Geschichte ergeben. Leerzeichen und Satzzeichen sowie einige Buchstaben sind schon vorgegeben. 

"""


def find_possible(blank, words):
    """
    find possible words of a list that fit into the blank given
    Finde alle möglichen Wörter von einer Liste, die in die gegebene Lücke passen könnten
    :param blank: Lücke zum Füllen
    :param words: Liste der Wörter
    :return: Liste von Wörtern, die in die Lücke passen. Wenn kein Wort passt wird eine leere Liste ausgegeben
    """
    possible = list()
    for word in words:
        # Das Wort passt in die Lücke wenn das Wort gleich lang ist wie die Lücke und die Differenz der beiden Strings
        # der Anzahl der felder ohne Buchstabe entspricht
        if len(blank) == len(word) and len(subtract_string(word, blank)) == blank.count("_"):
            possible.append(word)
    return possible


def subtract_string(s1, s2):
    """
    Differenz zweier Strings, beide Strings müssen gleich lang sein
    :param s1:
    :param s2:
    :return: String mit den Charakteren von s1, welche nicht an der selben Stelle in s2 sind
    """
    s3 = str()
    assert len(s1) == len(s2)
    for i in range(len(s1)):
        if s1[i] is not s2[i]:
            s3 += s1[i]
    return s3


def complete(_riddle, _words):
    # Die Satzzeichen werden vorher extrahiert und nacher wieder eingesetzt um das handling einfacher zu machen
    # punctuations ist eine Liste von Tupeln bestehend aus Index und dem Satzzeichen selbst
    punctuations = list()
    riddle = str()
    for i, val in enumerate(_riddle):
        if val in "!?.,;":
            punctuations.append((i, val))
        else:
            riddle += val

    riddle = riddle.split()
    words = _words[:]
    # Ein Counter wird benutzt um zu wissen, wie oft man ein gegebenes Wort einsetzen kann, da es auch Wörter gibt, die
    # sich mehrere male in der Wortliste befinden
    counter = Counter(words)

    # Diese Liste enthält den gelösten Satz
    solved_path = list()

    # index des Wortes was gerade versucht wird zu füllen
    index = 0
    # Visited hält alle schon besuchten Möglichkeiten von Kombinationen fest um das Rätsel zu lösen
    visited = set()
    while len(solved_path) < len(riddle):
        # Der Algorithmus findet wie eine Art Pfad durch ein Labyrinth
        # Dies ist gerade die Lücke zu füllen. Es started also bei Lücke null und versucht eine Lücke mit einem Wort zu
        # füllen. Dann wird ein möglicher Lösungssatz ausgewählt und versucht die nächste Lücke zu füllen.
        blank = riddle[index]
        # Mögliche Wörter, die in die Lücke passen könnten
        possible = find_possible(blank, words)
        # Nun werden die möglichen Kombinationen aus dem bisherigen Satz (solved_path) mit den wieteren möglichen
        # Wörtern generiert. Hier ist wichtig, dass die mögliche Lösung nicht schon zu oft das Wort enthält, welches
        # dem Satz hinzugefügt wird. Dafür wird der Counter benötigt.
        possible_paths = [solved_path + [x] for x in possible if solved_path.count(x) < counter[x]]
        # Schaue, welche Pfade schon besucht worden sind mit einer set differenz
        to_visit = list(set([" ".join(x) for x in possible_paths]).difference(visited))
        if to_visit:
            # Wenn es neue Pfäde gibt, die noch nicht ausprobiert worden sind mit den Ausgewählten Wörtern, wird ein
            # Pfad ausgewählt und ihm gefolgt
            word = to_visit[0].split()[-1]
            # Dem gelösten Satz bisher wird das Wort was in die Lücke passt angehängt und in der nächsten Iteration wird
            # die nächste Lücke gelöst
            solved_path.append(word)
            # go to the next blank
            index += 1
        else:
            # Wenn es entweder kein Wort mehr gibt was in die jetzige Lücke passt (da es schon fälschlicherweise vorher
            # zu oft benutzt wurde) oder ich schon bei allen Paden die diesem Wort folgen könnten war, alse to_visit
            # keine Pfäde erhält, füge den jetzigen Pfad dem visited set hinzu, damit er nicht nochmal besucht wird
            visited.add(" ".join(solved_path))
            # gehe eine Lücke zurück und schaue dort nach möglichen Pfaden
            solved_path.pop()
            index -= 1

    # Es wird dem gelösten Pfad die Satzzeichen wieder hinzugefügt
    solved = " ".join(solved_path)
    for (key, val) in punctuations:
        solved = solved[:key] + val + solved[key:]

    return solved


if __name__ == '__main__':
    for i in range(5):
        # Es wird die Library codecs benutzt um die Umlaute aus den Textdateien richtig zu lesen, da man mit der
        # normalen open() Methode von dieser Python version nicht das Encoding angeben kann
        with codecs.open("../bwinf39-runde1/a1-Woerter-aufraeumen/beispieldaten/raetsel" + str(i) + ".txt", "r", "utf-8") as riddle_file:
            print("Rätsel ", i, ": ")
            riddle = riddle_file.readline()
            words = riddle_file.readline().split()
            print(riddle)
            print("Ausgefüllt: ", complete(riddle, words), "\n\n")
