"""
Create classes to track homeworks.

1. Homework - accepts howework text and deadline (datetime.timedelta)
Homework has a method, that tells if deadline has passed.

2. Student - can solve homework with `do_homework` method.
Raises DeadlineError with "You are late" message if deadline has passed

3. Teacher - can create homework with `create_homework`; check homework with `check_homework`.
Any teacher can create or check any homework (even if it was created by one of colleagues).

Homework are cached in dict-like structure named `homework_done`. Key is homework, values are 
solutions. Each student can only have one homework solution.

Teacher can `reset_results` - with argument it will reset results for specific homework, without - 
it clears the cache.

Homework is solved if solution has more than 5 symbols.

-------------------
Check file with tests to see how all these classes are used. You can create any additional classes 
you want.
"""

from typing import List, Tuple


class DeadlineError(Exception):
    def __init__(self, message="You are late"):
        self.message = message
        super().__init__(self.message)


class Homework:
    def __init__(self, deadline: int):
        self._deadline = deadline

    def check_deadline(self):
        if self._deadline < 0:
            raise DeadlineError("You are late")


class Person:
    def __init__(self, lastname: str, name: str):
        self.lastname = lastname
        self.name = name


class Teacher(Person):
    @staticmethod
    def create_homework(deadline: int) -> Homework:
        return Homework(deadline)


class Student(Person):
    @staticmethod
    def do_homework(homework: Homework, solution: str):
        homework.check_deadline()