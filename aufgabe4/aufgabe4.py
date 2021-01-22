"""
the porblem requires the solution of the longest common path in both graph representations of the match figures
heuristik:
    - find all possible paths in both graph except paths with length one
    - try to find the length of the longest match between the the paths
    -  rotate the paths to be able to cover every possibility

example adjazenz: {"A": {"B": 0, "D": 90}, "B": {"A": 0, "C": 90}, "C": {"B": 90, "D": 0, "E": 120}, "D": {"A": 90, "C": 0, "E": 60}, "E": {"C": 120, "D": 60}, "F": {"E": 90}}
"""


class Aufstellung:
    """
    Hilfsklasse, enthält eine Aufstellung eines Bildes aus Streichhölzern mit einer Adjazenzliste wie dieser:
    {"A": {"B": 0, "D": 90}, "B": {"A": 0, "C": 90}, "C": {"B": 90, "D": 0, "E": 120}, "D": {"A": 90, "C": 0, "E": 60},
    "E": {"C": 120, "D": 60}, "F": {"E": 90}}
    """
    def __init__(self, adjazenz, n):
        self.adjazenz = adjazenz
        self.nodes = adjazenz.keys()
        self.n = n


class Streicholzrätsel:
    """
    Rästel Klasse enthält die Aufstellung von vorher und nacher. Wird dazu benutzt um die verschiedenen Methoden zu
    organisieren.
    """
    def __init__(self, vorher, n_vorher, nacher, n_nacher):
        """
        Initialisiert das Problem und erstellt die vorher und nacher Aufstellungen
        :param vorher: Adjazenzliste des vorher Bildes
        :param n_vorher: Streichölzer vorher im Bild
        :param nacher: Adjazenzliste des nacher Bildes
        :param n_nacher: Streichölzer nacher im Bild
        """
        self.vorher = Aufstellung(vorher, n_vorher)
        self.nacher = Aufstellung(nacher, n_nacher)

    def solve(self, turns):
        """
        Solve gibt aus ob es möglich ist die Streichhölzer in der gegebenen Anzahl an Umstellungen in das nacher Bild zu
        verwandeln
        :param turns: Nummer an Veränderung, die man machen darf
        :return:
        """
        # Wenn sich die Nummer an Streichölzern verändert hat, kann keine Lösung gefunden werden
        if self.vorher.n is not self.nacher.n:
            return False, [], "Comment: Not the same number of matches, not possible"
        # do some rotatig ?
        # Es wird die längste, gleiche Strikur in der
        longest_match, length = Streicholzrätsel.retrieve_longest_same_structures(self.vorher, self.nacher)
        min_turns = self.vorher.n - (length - 1)
        if turns - min_turns < 0:
            return False, [], "Comment: No enough turns, not possible"
        else:
            return True, longest_match, "Comment: Possible in " + str(min_turns) + "/" + str(turns) + " turns."

    def rotate_aufstellung(self):
        pass

    @staticmethod
    def retrieve_longest_same_structures(a, b):
        matches = list()
        for a_node in a.nodes:
            # check for every node in b if they have the same connection as a_node to another node
            for b_node in b.nodes:
                for a_key, a_value in a.adjazenz[a_node].items():
                    for b_key, b_value in b.adjazenz[b_node].items():
                        match = list()
                        if a_value == b_value:
                            # found a match of the first edge
                            match = [[[a_node, a_key], [b_node, b_key]]]
                            # search if this match leads somewhere
                            dead_end = False
                            new_matches = list(match)
                            while not dead_end:
                                dead_end = True
                                match = list(new_matches)
                                new_matches = list()
                                for i in range(len(match)):
                                    for k1, v1 in a.adjazenz[match[i][0][-1]].items():
                                        for k2, v2 in b.adjazenz[match[i][1][-1]].items():
                                            # make sure its not going back or looping around
                                            if k1 is not match[i][0][-1] and k2 is not match[i][1][-1] and k1 not in match[i][0] and k2 not in match[i][1]:
                                                if v1 == v2:
                                                    dead_end = False
                                                    # doead end is not met by at least one node connection
                                                    # append to new match list with lengthened paths
                                                    new_match = list(match)
                                                    new_match[i][0].append(k1)
                                                    new_match[i][1].append(k2)
                                                    new_matches.append([new_match[i][0], new_match[i][1]])
                            matches += list(match)
        # now grab the longest matching path of the match list
        longest_match = max(matches, key=lambda x: len(x[0]))
        return longest_match, len(longest_match[0])


if __name__ == '__main__':
    aufstellung1 = {"A": {"B": 0, "D": 90}, "B": {"A": 0, "C": 90}, "C": {"B": 90, "D": 0, "E": 120}, "D": {"A": 90, "C": 0, "E": 60}, "E": {"C": 120, "D": 60}, "F": {"E": 90}}
    aufstellung2 = {"A": {"C": 60, "E": 90}, "B": {"C": 120, "D": 90}, "C": {"A": 60, "B": 120, "F": 90}, "D": {"B": 90, "F": 120}, "E": {"A": 90, "F": 60}, "F": {"C": 90, "D": 120, "E": 60}}

    # Streicholzrätsel.retrieve_all_same_structures(aufstellung1, aufstellung2)
    s = Streicholzrätsel(aufstellung1, 7, aufstellung2, 7)
    print(s.solve(5))
