"""
Create a new database named "films_db".
Use the SQLAlchemy library to create the database and tables in Python.
Part 1: Setting up the Database
Create one table for films, with the following columns:
    films table:
        id (integer, primary key)
        title (string)
        director (string)
        release year (integer)
Part 2: Manipulating with Database
    Create script that:
        Add 3 film to the film table.
        Update 1 film
        Print data from table
        Delete all data from table
"""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select, asc, delete
from sqlalchemy.orm import relationship, Session, Mapped, DeclarativeBase
from typing import List


class Base(DeclarativeBase):
    pass


class DB:
    def __init__(self, file_name):
        self.engine = create_engine(f'sqlite:///{file_name}')

    def __enter__(self):
        self.session = Session(self.engine)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()


class Director(Base):
    __tablename__ = 'directors'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(32), unique=True)
    films = relationship("Film", back_populates="director")

    def __repr__(self) -> str:
        return f"Director(id={self.id!r}, director={self.director!r})"


class Film(Base):
    __tablename__ = 'films'

    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String(128), unique=True)
    director_id: Mapped[int] = Column(Integer, ForeignKey('directors.id'))
    year: Mapped[int] = Column(Integer)
    director = relationship("Director", back_populates="films")

    def __repr__(self) -> str:
        return f"Film(id={self.id!r}, title={self.title!r}, director={self.director.name!r}, release_year={self.year!r})"


def create_tables(db: DB):
    Base.metadata.create_all(db.engine)


def add_table_data(db: DB):
    directors = [
        Director(name='Ridley Scott'),
        Director(name='James Cameron'),
        Director(name='David Fincher'),
        Director(name='Andy Wachowski, Larry Wachowski')
    ]
    db.session.add_all(directors)
    db.session.commit()

    films = [
        Film(title='Alien', director_id=directors[0].id, year=1979),
        Film(title='Terminator 2', director_id=directors[1].id, year=1991),
        Film(title='Se7en', director_id=directors[2].id, year=1995),
        Film(title='Fight Club', director_id=directors[2].id, year=1999),
        Film(title='The Matrix', director_id=directors[3].id, year=1999)
    ]
    db.session.add_all(films)
    db.session.commit()


def modify_table_data(db: DB):
    stmt = select(Director).where(Director.name == 'Andy Wachowski, Larry Wachowski')
    db.session.scalars(stmt).one().name = 'Lana Wachowski, Lilly Wachowski'
    db.session.commit()


def print_table_data(db: DB) -> List[str]:
    films = []
    stmt = select(Film).order_by(asc(Film.id))
    for film in db.session.scalars(stmt).all():
        print(film)
        films.append(str(film))

    return films


def delete_tables(db):
    db.session.execute(delete(Film))
    db.session.execute(delete(Director))
    db.session.commit()


def drop_database(db):
    Base.metadata.drop_all(db.engine)
