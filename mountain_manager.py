from typing import List

from algorithms.mergesort import mergesort
from mountain import Mountain
from data_structures.hash_table import *

class MountainManager:
    def __init__(self) -> None:
        """
        Complexity:
        #worst case: O(1), creating hash table and initialised it
        #best case: O(1), same as worst case
        """
        self.mountain_table = LinearProbeTable[str, Mountain]()

    def add_mountain(self, mountain: Mountain) -> None:
        """
        Complexity:
        #worst case: O(1), everything is constant
        #best case: O(1), everything is constant
        """
        self.mountain_table[mountain.name] = mountain

    def remove_mountain(self, mountain: Mountain) -> None:
        """
        Complexity:
        #worst case: O(1), everything is constant
        #best case: O(1), everything is constant
        """
        del self.mountain_table[mountain.name]

    def edit_mountain(self, old_mountain: Mountain, new_mountain: Mountain) -> None:
        """
         Complexity:
        #worst case: O(1), everything is constant
        #best case: O(1), everything is constant
        """
        del self.mountain_table[old_mountain.name]
        self.mountain_table[new_mountain.name] = new_mountain

    def mountains_with_difficulty(self, diff: int) -> List[Mountain]:
        """
        Complexity:
        #worst case: O(n), where n is the number of elements in self.mountain_table.values()
        #best case: O(1), when there is only 1 element in self.mountain_table.values()
        """
        mountains = []
        for mountain in self.mountain_table.values():
            if mountain.difficulty_level == diff:
                mountains.append(mountain)
        return mountains

    def group_by_difficulty(self) -> List[List[Mountain]]:
        """
        Complexity:
        #worst case: O(n), where n is the number of elements in self.mountain_table.values()
        #best case: O(1), when there is only 1 element in self.mountain_table.values()
        """

        max_difficulty = max(mountain.difficulty_level for mountain in self.mountain_table.values())

        grouped_mountains = [[] for _ in range(max_difficulty + 1)]

        for mountain in self.mountain_table.values():
            difficulty = mountain.difficulty_level
            grouped_mountains[difficulty].append(mountain)

        grouped_mountains = [grouped_mountains for grouped_mountains in grouped_mountains if grouped_mountains]

        for i in range(len(grouped_mountains)):
            grouped_mountains[i] = mergesort(grouped_mountains[i], key1=lambda x: x.length, key2=lambda x: x.name)

        return grouped_mountains