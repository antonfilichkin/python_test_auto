import pytest

from hw5_2 import *
import sqlite3

conn = sqlite3.connect('example.sqlite')


@pytest.fixture
def books_count():
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM books")
    return cursor.fetchone()[0]


@pytest.fixture
def books_bradbury():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM books WHERE author = 'Bradbury'")
    return cursor.fetchone()[0]


@pytest.fixture
def books_authors():
    cursor = conn.cursor()
    cursor.execute("SELECT author FROM books ORDER BY author")
    return iter(tuple(row[0] for row in cursor.fetchall()))


def test_table_data_return_expected_length(books_count):
    books = TableData('example.sqlite', 'books')
    assert len(books) == books_count


def test_table_data_return_value(books_bradbury):
    books = TableData('example.sqlite', 'books')
    assert books['Bradbury'] == books_bradbury


def test_table_data_return_if_author_is_present():
    books = TableData('example.sqlite', 'books')
    assert 'Rowling' not in books
    assert 'Bradbury' in books


def test_table_data_iteration(books_authors):
    books = TableData('example.sqlite', 'books')
    for book in books:
        assert book['author'] == next(books_authors)
