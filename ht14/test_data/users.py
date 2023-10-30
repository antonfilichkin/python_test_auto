from pytest import fixture


class User:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password


@fixture
def existing_user():
    return type('User', (object,), {'name': 'Name27102023', 'password': 'Name27102023'})
