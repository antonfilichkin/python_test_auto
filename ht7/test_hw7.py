import pytest
import os

from typing import Type
from sqlalchemy import MetaData, desc
from hw7 import *


@pytest.fixture(scope='session')
def delete_db(request):
    if os.path.exists('films.db'):
        os.remove('films.db')


@pytest.mark.run(order=1)
def test_create_table():

    with DB('films.db') as db:
        create_tables(db)

        metadata = MetaData()
        metadata.reflect(db.engine)

        assert sorted([table.name for table in metadata.tables.values()]) == ['directors', 'films']


@pytest.mark.run(order=2)
def test_add_table_data():

    with DB('films.db') as db:
        add_table_data(db)

        film = db.session.query(Film).\
            filter(Film.director.has(name='David Fincher')).\
            order_by(desc(Film.title)).\
            first()

        assert (film.title, film.director.name) == ('Se7en', 'David Fincher')


@pytest.mark.run(order=3)
def test_modify_table_data():

    with (DB('films.db') as db):
        assert _get_film_director(db, 'The Matrix') == 'Andy Wachowski, Larry Wachowski'
        modify_table_data(db)
        assert _get_film_director(db, 'The Matrix') == 'Lana Wachowski, Lilly Wachowski'


def _get_film_director(db: DB, film: str) -> str:
    return db.session.query(Film).\
        filter(Film.title == f'{film}').\
        first().\
        director.name


@pytest.mark.run(order=4)
def test_print_table_data():
    with (DB('films.db') as db):
        assert print_table_data(db) == [
            "Film(id=1, title='Alien', director='Ridley Scott', release_year=1979)",
            "Film(id=2, title='Terminator 2', director='James Cameron', release_year=1991)",
            "Film(id=3, title='Se7en', director='David Fincher', release_year=1995)",
            "Film(id=4, title='Fight Club', director='David Fincher', release_year=1999)",
            "Film(id=5, title='The Matrix', director='Lana Wachowski, Lilly Wachowski', release_year=1999)"
        ]


@pytest.mark.run(order=5)
def test_delete_table_data():
    with (DB('films.db') as db):
        assert _get_table_count(db, Film) == 5
        assert _get_table_count(db, Director) == 4

        delete_tables(db)

        assert _get_table_count(db, Film) == 0
        assert _get_table_count(db, Director) == 0

        drop_database(db)

        metadata = MetaData()
        metadata.reflect(db.engine)

        assert not metadata.tables


def _get_table_count(db: DB, table: Type) -> int:
    return db.session.query(table).count()
