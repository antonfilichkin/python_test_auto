"""
Write a wrapper class TableData for database table, that when initialized with database name and table acts as collection object (implements Collection protocol).
Assume all data has unique values in 'author' column.
So, if books = TableData(database_name='example.sqlite', table_name='books')

then
 -  `len(books)` will give current amount of rows in books table in database
 -  `books['Bradbury']` should return single data row for book with author Bradbury
 -  `'Yeltsin' in books` should return if book with same author exists in table
 -  object implements iteration protocol. i.e. you could use it in for loops::
       for book in books:
           print(book['author'])
 - all above mentioned calls should reflect most recent data. If data in table changed after you created collection instance, your calls should return updated data.

Avoid reading entire table into memory. When iterating through records, start reading the first record, then go to the next one, until records are exhausted.
When writing tests, it's not always neccessary to mock database calls completely. Use supplied example.sqlite file as database fixture file.
"""
import sqlite3


class TableData:

    def __init__(self, database_name: str, table_name: str):
        self.__connection__ = sqlite3.connect(database_name)
        self.__connection__.row_factory = sqlite3.Row
        self.__table__ = table_name

    def __del__(self):
        self.__connection__.close()

    def __fetchone__(self, *args):
        cursor = self.__connection__.cursor()
        cursor.execute(*args)
        return cursor.fetchone()

    def __len__(self):
        return self.__fetchone__(f"SELECT count(*) FROM {self.__table__}")['count(*)']

    def __getitem__(self, key):
        return self.__fetchone__(f"SELECT name FROM {self.__table__} WHERE author = ?", (key,))['name']

    def __contains__(self, key):
        return self.__fetchone__(f"SELECT * FROM {self.__table__} WHERE author = ?", (key,)) is not None

    def __iter__(self):
        self.__iter_cursor__ = self.__connection__.cursor()
        self.__iter_cursor__.execute(f"SELECT * FROM {self.__table__} ORDER BY author")
        return self

    def __next__(self):
        self.__row__ = self.__iter_cursor__.fetchone()
        if self.__row__ is None:
            raise StopIteration
        else:
            return dict(self.__row__)
