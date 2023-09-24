"""
We have a file that works as key-value storage, each line is represented as key and value separated by = symbol, example:

name=kek
last_name=top
song_name=shadilay
power=9001

Values can be strings or integer numbers. If a value can be treated both as a number and a string, it is treated as number.

Write a wrapper class for this key value storage that works like this:

storage = KeyValueStorage('path_to_file.txt')
that has its keys and values accessible as collection items and as attributes.
Example:
storage['name']  # will be string 'kek'
storage.song_name  # will be 'shadilay'
storage.power  # will be integer 9001

In case of attribute clash existing built-in attributes take precedence.
In case when value cannot be assigned to an attribute (for example when there's a line `1=something`) ValueError should be raised.
File size is expected to be small, you are permitted to read it entirely into memory.

"""
import keyword
import re


class KeyValueStorage:
    """Class docstring"""

    __valid_name_pattern__ = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

    @classmethod
    def __is_valid_attribute_name__(cls, string: str) -> bool:
        if cls.__valid_name_pattern__.match(string):
            return not keyword.iskeyword(string)

    @classmethod
    def __is_digit__(cls, string: str) -> bool:
        return string.isdigit() or string[0] in ('-', '+') and string[1:].isdigit()

    @classmethod
    def __parse_input_string__(cls, input_string: str) -> (str, object):
        key, value = input_string.strip().split("=", 1)
        if not cls.__is_valid_attribute_name__(key):
            raise ValueError("Attribute name is not allowed! Provided '{}'".format(input_string))
        if cls.__is_digit__(value):
            value = int(value)
        return key, value

    def __init__(self, input_file: str):
        with open(input_file, 'r') as file:
            for line in file:
                key, value = KeyValueStorage.__parse_input_string__(line)
                if key not in dir(self) and key not in self.__dict__:
                    self.__dict__.update({key: value})

    def __getitem__(self, item):
        return self.__dict__.get(item)
