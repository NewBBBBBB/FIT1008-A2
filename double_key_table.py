from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')


class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241,
                   786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes: list | None = None, internal_sizes: list | None = None) -> None:
        """
        Complexity:
        #worst case: O(1), creating array and initialised class variables
        #best case: O(1), same as worst case
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes
        self.size_index = 0
        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0
        self.internal_sizes = internal_sizes

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Complexity
        #worst case: O(n), where n represents the number of elements in self.table_size
        #best case: O(1), where there is only 1 element in self.table_size
        """
        outer_position = self.hash1(key1)
        inner_table = None
        for _ in range(self.table_size):
            if self.array[outer_position] is None:
                if is_insert:
                    inner_table = LinearProbeTable(self.internal_sizes)
                    self.array[outer_position]=(key1,inner_table)
                    inner_table.hash = lambda k:self.hash2(k,inner_table)
                    inner_position = self.array[outer_position][1]._linear_probe(key2, is_insert)
                    return outer_position, inner_position
                else:
                    raise KeyError(key1)
            elif self.array[outer_position][0] == key1:
                inner_position = self.array[outer_position][1]._linear_probe(key2, is_insert)
                return outer_position, inner_position
            else:
                outer_position = (outer_position + 1) % self.table_size

        if is_insert:
            raise FullError("Table is full!")
    def iter_keys(self, key: K1 | None = None) -> Iterator[K1 | K2]:
            """
            key = None:
                Returns an iterator of all top-level keys in hash table
            key = k:
                Returns an iterator of all keys in the bottom-hash-table for k.
            Complexity
            #worst case: O(n), where n represents the number of keys in self.array
            #best case: O(1), where there is only one key inside self.array
            """
            if key is None:
                for item in self.array:
                    if item is not None:
                        yield item[0]
            else:
                for item in self.array:
                    if item is not None and item[0] == key:
                        yield from item[1].keys()

    def keys(self, key: K1 | None = None) -> list[K1]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        Complexity
        # worst case: O(n), where n represents the number of keys in self.table_size
        # best case: O(1), where there is only one key inside self.table_size
        """

        keys = []
        if key is None:
            for i in range(self.table_size):
                if self.array[i] is not None:
                    keys.append(self.array[i][0])
            return keys
        else:
            for i in range(self.table_size):
                if self.array[i] is not None and self.array[i][0]==key:
                    return self.array[i][1].keys()

    def iter_values(self, key: K1 | None = None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        Complexity
        # worst case: O(n), where n represents the number of values in self.array
        # best case: O(1), where there is only one value inside self.array
        """

        if key is None:
            for item in self.array:
                if item is not None:
                    yield from item[1].values()
        else:
            for item in self.array:
                if item is not None and item[0] == key:
                    yield from item[1].values()

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        Complexity
        # worst case: O(n), where n represents the number of values in self.array
        # best case: O(1), where there is only one value inside self.array
        """

        values = []
        if key is None:
            for item in self.array:
                if item is not None:
                    values.extend(item[1].values())
            return values
        else:
            for i in range(self.table_size):
                if self.array[i] is not None and self.array[i][0] == key:
                    inner_table = self.array[i][1]
                    return inner_table.values()

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.

        Complexity:
        # worst case: O(n), as it called linear probe which has worst case complexity of O(n),
        # where n represents the number of elements in self.table_size
        #best case: O(1),everything including calling linear probe is constant
        """
        outer_position,inner_position = self._linear_probe(key[0],key[1],False)
        if self.array[outer_position] is not None and self.array[outer_position][0]==key[0]:
            inner_table = self.array[outer_position][1]
            return inner_table[inner_position]
        else:
            raise KeyError(key)


    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        Complexity
        # worst case: O(n), as it called linear probe which has worst case complexity of O(n),
        # where n represents the number of elements in self.table_size
        #best case: O(1),everything including calling linear probe is constant
        """

        outer_position,inner_position = self._linear_probe(key[0], key[1], True)

        inner_table = self.array[outer_position][1]
        if self.array[outer_position][0] is None:
            self.array[outer_position] = (key[0], inner_table)

        elif len(self.array[outer_position][1].keys()) == 0:
            self.count += 1

        inner_table[key[1]] = data

        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        Complexity
        # worst case: O(n*m), as it called linear probe which has worst case complexity of O(n),
        # where n represents the number of elements in self.outer.table, m represents number of elements in
        # inner table
        # best case: O(1),everything including calling linear probe is constant
        """

        outer_position, inner_position = self._linear_probe(key[0], key[1], False)
        inner_table = self.array[outer_position][1]
        if inner_position is not None:
            if inner_table.keys() == [key[1]]:
                self.array[outer_position] = None
                self.count -= 1
            else:
                del inner_table[key[1]]

        position = (outer_position + 1) % self.table_size
        while self.array[position] is not None:
            key2, value = self.array[position]
            for i in self.iter_keys(key2):
                new_outer_pos, new_inner_pos = self._linear_probe(key2, i, True)
                self.array[new_outer_pos][1][i] = value
            position = (position + 1) % self.table_size

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        old_array = self.array
        self.size_index += 1
        new_size = self.TABLE_SIZES[self.size_index]

        # Create a new array with the doubled size
        self.array = ArrayR(new_size)
        self.array.hash = lambda k:self.hash1(k)
        self.count = 0
        # Rehash and reinsert all values
        for tuples in old_array:
            if tuples is not None:
                key, inner_table = tuples
                keys_list = inner_table.keys()
                values_list = inner_table.values()
                for i in range(len(inner_table.keys())):
                    key1 = key
                    key2 = keys_list[i]
                    value = values_list[i]
                    self[(key1, key2)] = value

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)

        Complexity:
        # worst case: O(1), everything is constant
        # best case: O(1), everything is constant
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table

        Complexity:
        # worst case: O(1), everything is constant
        # best case: O(1), everything is constant
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        pass