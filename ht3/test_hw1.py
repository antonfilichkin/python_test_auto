import os

import pytest
from hw1 import check_data, validate_date, validate_line

data = [
    "baz@example.com 729.83 USD accountName 2021-01-02",
    "foo@example.com 729.83 EUR accountName 2021-01:0",
    "bar@example.com 729.83 accountName 2021-01-02",
    "baz@example.com 729.83 USD accountName ABCD-01-02",
    "baz@example.com 729.83 USD accountName 2021--02",
    "baz@example.com 729.83 USD accountName 2021:01:02",
    "baz@example.com 729.83 USD 2021-01-",
    "baz@example.com 729.83 USD accountName !!!:{{:{{",
    "2021-01-02",
]


@pytest.fixture
def file_path():
    filepath = "small_file"
    with open(filepath, "w+", encoding="utf-8") as f:
        for line in data:
            f.write(line + "\n")

    yield filepath
    os.remove(os.path.abspath(filepath))


def test_check_data(file_path):
    result_path = check_data(file_path, [validate_date, validate_line])
    with open(result_path) as res:
        for i, line in enumerate(res, start=1):
            assert line.rsplit(" ", 1)[0] in data

    assert i == len(data) - 1


def test_check_data_real_file():
    result_path = check_data("data.txt", [validate_date, validate_line])
    with open(result_path) as res:
        for i, _ in enumerate(res, start=1):
            pass
    assert i == 777
