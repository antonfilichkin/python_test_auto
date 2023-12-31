"""
Given an array of size n, find the most common and the least common elements.
The most common element is the element that appears more than n // 2 times.
The least common element is the element that appears fewer than other.

You may assume that the array is non-empty and the most common element
always exist in the array.

Example 1:

Input: [3,2,3]
Output: 3, 2

Example 2:

Input: [2,2,1,1,1,2,2]
Output: 2, 1

"""
from collections import Counter
from typing import List, Tuple


def major_and_minor_elem(inp: List) -> Tuple[int, int]:
    counter = Counter(inp).most_common()
    return counter[0][0], counter[-1][0]


def major_and_minor_elem_2(inp: List) -> Tuple[int, int]:
    elements_count = {}
    for element in inp:
        elements_count[element] = elements_count.get(element, 0) + 1

    elements_count_sorted = sorted(elements_count, key=elements_count.get)
    return elements_count_sorted[-1], elements_count_sorted[0]