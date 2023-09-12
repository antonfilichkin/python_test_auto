import pytest

from hw1_1 import major_and_minor_elem, major_and_minor_elem_2

LISTS = [
    ([2, 2, 1, 1, 1, 2, 2], (2, 1)),
    ([3, 2, 3], (3, 2)),
    ([3, 3, 2, 2, 3, 3, 1], (3, 1)),
    ([1], (1, 1)),
    ([3, 3, 3, 3, 3, 3, 1, 8, 9, 1, 9], (3, 8))
    # ([3, 3, 3, 4, 4, 4, 1, 1, 2, 2], (4, 1)) // Should we handle such a cases?
]


@pytest.mark.parametrize("numbers, expected", LISTS)
def test_major_and_minor_elem(numbers, expected):
    assert major_and_minor_elem(numbers) == expected


@pytest.mark.parametrize("numbers, expected", LISTS)
def test_major_and_minor_elem_2(numbers, expected):
    assert major_and_minor_elem_2(numbers) == expected
