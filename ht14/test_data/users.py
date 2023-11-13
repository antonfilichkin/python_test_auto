from dataclasses import dataclass
from pytest import fixture


@dataclass
class User:
    name: str
    password: str


@fixture
def existing_user():
    return User('Name27102023', 'Name27102023')
