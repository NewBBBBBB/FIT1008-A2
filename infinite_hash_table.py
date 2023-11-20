from __future__ import annotations
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self) -> None:
        """
        Complexity:
        worst case: O(1), initialisation of variables
        best case: O(1)
        """
        self.level = 0
        self.key_list = []
        self.index_list = []
        self.hash_key_list = []

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Complexity:
        #worst complexity: O(1), everything is constant
        #best complexity: O(1), everything is constant
        """

        try:
            index = self.key_list.index(key)
            return self.index_list[index]
        except ValueError:
            raise KeyError(key)

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Complexity:
        #worst complexity: O(1), everything is constant
        #best complexity: O(1), everything is constant
        """

        self.key_list.append(key)
        self.index_list.append(value)

        self.level = 0
        hashlist = []
        for i in (key[:4]):
            hashlist.append(self.hash(key))
            self.level += 1
        if len(hashlist) < 4:
            hashlist.append(26)
        self.hash_key_list.append(hashlist)

        # print(self.key_list, self.index_list, self.hash_key_list)
        # raise NotImplementedError()

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Complexity:
        #best complexity: O(1)
        #worst complexity: O(n), where n is the length of the list, where the key to be deleted is found last in the key_list

        """

        try:
            self.hash_key_list.pop(self.key_list.index(key))
            self.key_list.remove(key)
            self.index_list.pop()
        except ValueError:
            raise KeyError

    def __len__(self):
        """"
        Complexity:
        # worst complexity: O(1), everything is constant
        # best complexity: O(1), everything is constant
        """
        return len(self.key_list)

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """

        result = ""
        for i in self.key_list:
            result += "(" + i + "," + str(self.index_list[self.key_list.index(i)]) + ")\n"

        return result


    def get_location(self, key):
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.

        Complexity:
        #best-case complexity: O(1)
        #Worst-case complexity: O(n*m), where n is the length of the key_list, m is the length of char
        # where the key is found last in the key_list
        """
        try:
            hash_list = self.hash_key_list[self.key_list.index(key)]
            #print(self.hash_key_list[self.key_list.index(key)])
            length_match = 1
            for Key in self.key_list:
                if key == Key:
                    #print(Key,key)
                    continue
                match = ""
                for i in range(min(len(Key), len(key))):
                    if Key[i] == key[i]:
                        #print(Key[i], key[i])
                        match += Key[i]
                        #print(match)
                        if length_match < len(match) + 1:
                            length_match = len(match) + 1
                            #print(length_match)
                    else:
                        break
                    # print(length_match)

            # print(self.hash_key_list)
            return self.hash_key_list[self.key_list.index(key)][:min(length_match, 4)]
        except ValueError:
            raise KeyError