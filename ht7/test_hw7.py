import pytest
import os

from typing import Type
from sqlalchemy import MetaData, desc, func
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

        stmt = select(Film).where(Film.director.has(name='David Fincher')).order_by(desc(Film.title))

        for expected_film, film in zip([('Se7en', 'David Fincher'), ('Fight Club', 'David Fincher')], db.session.scalars(stmt).all()):
            assert (film.title, film.director.name) == expected_film


@pytest.mark.run(order=3)
def test_modify_table_data():
    stmt = select(Film).where(Film.title == 'The Matrix')

    with (DB('films.db') as db):
        assert db.session.scalars(stmt).one().director.name == 'Andy Wachowski, Larry Wachowski'
        modify_table_data(db)
        assert db.session.scalars(stmt).one().director.name == 'Lana Wachowski, Lilly Wachowski'


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
    stmt = select(func.count()).select_from(table)
    return db.session.execute(stmt).scalar()
