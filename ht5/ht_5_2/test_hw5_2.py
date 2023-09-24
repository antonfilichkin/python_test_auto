import pytest

from hw5_2 import *
import sqlite3


conn = sqlite3.connect('example.sqlite')
cursor = conn.cursor()


@pytest.fixture
def books_count():
    cursor.execute('SELECT count(*) FROM books')
    return cursor.fetchone()[0]

# @pytest.fixture
# def bradbury():
#     conn = sqlite3.connect('example.sqlite')
#     cursor = conn.cursor()
#     # cursor.execute('SELECT * from TABLE1')
#     cursor.execute('SELECT * FROM books WHERE author = ?', ('Bradbury',))
#     cursor.execute('SELECT count() FROM books')
#     return cursor.fetchall()


def test_table_data_return_expected_length(books_count):
    book = TableData('example.sqlite', 'books')
    assert len(book) == books_count











 # -  `len(books)` will give current amount of rows in books table in database
 # -  `books['Bradbury']` should return single data row for book with author Bradbury
 # -  `'Yeltsin' in books` should return if book with same author exists in table
 # -  object implements iteration protocol. i.e. you could use it in for loops::
 #       for book in books:
 #           print(book['author'])