import pytest

from hw_ig import merge_elems, map_like

MERGE = [
    (
        [[1, 2, 3], 6, 'zhaba', [[1, 2], [3, 4]]],
        [1, 2, 3, 6, 'z', 'h', 'a', 'b', 'a', 1, 2, 3, 4]
    ),
    (
        [[1, 2, 3, [4, 5], [6, 7, 8]], 9, 'ten', [[11, (12, (13, 14, (15, 16, [17]))), [18, 19], 20]]],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 't', 'e', 'n', 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    )
]

MAP = [
    (
        [[1, 2, 3], 6, 'zhaba', True],
        lambda x: x[0],
        [1, "6: 'int' object is not subscriptable", 'z', "True: 'bool' object is not subscriptable"]
    )
]


@pytest.mark.parametrize("test_data, expected_result", MERGE)
def test_merge_elems(test_data, expected_result):
    actual_result = []
    for _ in merge_elems(*test_data):
        actual_result.append(_)
        print(_, end=' ')

    assert actual_result == expected_result


@pytest.mark.parametrize("test_data, fun, expected_result", MAP)
def test_map_like(test_data, fun, expected_result):
    actual_result = []
    for _ in map_like(fun, *test_data):
        actual_result.append(_)
        print(_)

    assert actual_result == expected_result
