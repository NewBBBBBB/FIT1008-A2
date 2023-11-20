from __future__ import annotations
from typing import TypeVar


T = TypeVar("T")

def merge(l1: list[T], l2: list[T], key1=lambda x: x.length, key2=lambda x: x.name) -> list[T]:
    """
    Merges two sorted lists of Mountain objects into one larger sorted list,
    containing all elements from the smaller lists.

    The `key` kwarg allows you to define a custom sorting order.
    By default, the function sorts the Mountains by their difficulty level.

    :pre: Both l1 and l2 are sorted, and contain comparable elements.
    :complexity: Best/Worst Case O(n * comp(T)), n = len(l1)+len(l2)
    :returns: The sorted list.
    """
    new_list = []
    cur_left = 0
    cur_right = 0
    while cur_left < len(l1) and cur_right < len(l2):
        if key1(l1[cur_left]) < key1(l2[cur_right]):
            new_list.append(l1[cur_left])
            cur_left += 1
        elif key1(l1[cur_left]) > key1(l2[cur_right]):
            new_list.append(l2[cur_right])
            cur_right += 1
        elif key1(l1[cur_left]) == key1(l2[cur_right]):
            if key2(l1[cur_left]) <= key2(l2[cur_right]):
                new_list.append(l1[cur_left])
                cur_left += 1
            else:
                new_list.append(l2[cur_right])
                cur_right += 1
    new_list += l1[cur_left:]
    new_list += l2[cur_right:]
    return new_list


def mergesort(l: list[T], key1=lambda x: x.length, key2=lambda x: x.name) -> list[T]:
    """
    Sort a list of Mountain objects using the mergesort algorithm.
    By default, the function sorts the Mountains by their difficulty level.

    :pre: l is a list of comparable Mountain objects.
    :complexity: Best/Worst Case O(NlogN * comp(T))
    """
    if len(l) <= 1:
        return l
    break_index = (len(l)+1) // 2
    l1 = mergesort(l[:break_index], key1=key1, key2=key2)
    l2 = mergesort(l[break_index:], key1=key1, key2=key2)
    return merge(l1, l2, key1=key1, key2=key2)