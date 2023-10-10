import pytest

from hw5_1 import *


def test_wrapper_dict():
    storage = KeyValueStorage('input1.txt')
    assert storage['name'] == 'kek'
    assert storage.song == 'shadilay'
    assert storage.power == 9001
    assert storage.negative_power == -9001


def test_wrapper_dict_should_not_overwrite_built_in():
    storage = KeyValueStorage('input1.txt')
    assert storage.__doc__ == 'Class docstring'


def test_wrapper_should_throw_error():
    with pytest.raises(ValueError, match="Attribute name is not allowed!"):
        KeyValueStorage('input2.txt')
