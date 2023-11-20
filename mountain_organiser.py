from __future__ import annotations

from algorithms.binary_search import *
from algorithms.mergesort import *

class MountainOrganiser:

    def __init__(self) -> None:
        """
        Complexity:
        #worst case: O(1), initialisation
        #best case: O(1), same as worst case
        """
        self.mountains = []

    def add_mountains(self, mountains: List[Mountain]) -> None: #mergesort O(Mlog(M)+N)
        """
        Complexity:
         worst case: O(Mlog(M)+N), where everything is constant, where N represents the length of mountains list
         best case, O(Mlog(M)+N), where everything is constant

        Note:
         mergesort algorithm is modified to take 2 keys which is mountain.name and mountain.length to sort them ascendingly
        """

        sorted_list = merge(mergesort(mountains),self.mountains)
        self.mountains = sorted_list

    def cur_position(self, mountain: Mountain) -> int: #binary search O(log(N)
        """
        Complexity:
         worst case: O(log(N)), where N is the length of the list of mountains.
         best case, O(1), when middle index contains item.

        Note:
         binary search algorithm is modified to make comparison between mountain length and name
        """
        if mountain not in self.mountains:
            raise KeyError(mountain)
        position = binary_search(self.mountains,mountain)
        return position

