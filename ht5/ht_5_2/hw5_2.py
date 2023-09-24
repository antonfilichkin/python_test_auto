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
        self.__conn__ = sqlite3.connect(database_name)
        self.table = table_name

    def __len__(self):
        cursor = self.__conn__.cursor()
        cursor.execute(f'SELECT count(*) FROM {self.table}')
        return cursor.fetchone()[0]

    # def __getitem__(self, key):
    #     if key in self.data:
    #         return self.data[key]
    #     else:
    #         raise KeyError(f"'{key}' not found in MyIterable")
    #
    # def __iter__(self):
    #     return
    #
    # def __next__(self):
    #     if self.current_value > self.max_value:
    #         # When there are no more items to iterate, raise StopIteration.
    #         raise StopIteration
    #     else:
    #         result = self.current_value
    #         self.current_value += 1
    #         return result
