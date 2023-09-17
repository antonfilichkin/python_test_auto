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

from typing import Dict, Set


class DeadlineError(Exception):
    def __init__(self, message="You are late"):
        self.message = message
        super().__init__(self.message)


class Homework:
    def __init__(self, name: str, deadline: int):
        self._name = name
        self._deadline = deadline

    def check_deadline(self):
        if self._deadline < 0:
            raise DeadlineError("You are late")


class Solution:
    def __init__(self, author: 'Student', homework: Homework, solution: str):
        self.homework = homework
        self.author = author
        self.solution = solution


class Person:
    def __init__(self, lastname: str, name: str):
        self.lastname = lastname
        self.name = name


class Student(Person):
    def do_homework(self, homework: Homework, solution: str) -> Solution:
        homework.check_deadline()
        return Solution(self, homework, solution)


class Teacher(Person):
    homework_done: Dict[Homework, Set[Solution]] = {}

    @staticmethod
    def create_homework(task: str, deadline: int) -> Homework:
        return Homework(task, deadline)

    @classmethod
    def check_homework(cls, solution: Solution) -> bool:
        if solution.homework not in cls.homework_done:
            cls.homework_done[solution.homework] = set()

        if len(solution.solution) > 5:
            cls.homework_done[solution.homework].add(solution)
            return True
        else:
            return False

    @classmethod
    def reset_results(cls, homework: Homework = None):
        if homework is None:
            cls.homework_done.clear()
        else:
            cls.homework_done.pop(homework)
