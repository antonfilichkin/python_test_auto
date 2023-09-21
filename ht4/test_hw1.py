import pytest

from hw1 import *


@pytest.fixture
def prepare_test_classes():
    first_teacher = Teacher("Kay", "Alan")
    second_teacher = Teacher("Liskov", "Barbara")

    first_student = Student("Hopper", "Grace")
    second_student = Student("Turing", "Alan")

    first_hw = Teacher.create_homework("OOP homework", 1)
    second_hw = Teacher.create_homework("Read the documentation", 5)
    return (
        first_teacher,
        second_teacher,
        first_student,
        second_student,
        first_hw,
        second_hw,
    )


def test_deadline_exception():
    hw = Teacher.create_homework("Expired hw", -1)
    with pytest.raises(DeadlineError, match="You are late"):
        Student("Green", "Robert").do_homework(hw, "solution")


def test_oop(prepare_test_classes):
    (
        first_teacher,
        second_teacher,
        first_student,
        second_student,
        first_hw,
        second_hw,
    ) = prepare_test_classes

    result_1 = first_student.do_homework(first_hw, "Homework 1 is done")
    result_2 = second_student.do_homework(second_hw, "done")

    assert result_1.author == first_student
    assert result_2.author == second_student

    assert first_teacher.check_homework(result_1)

    hw_cache_length = len(Teacher.homework_done[first_hw])

    assert second_teacher.check_homework(result_1)
    assert hw_cache_length == len(Teacher.homework_done[first_hw]) == 1
    assert result_1 in Teacher.homework_done[first_hw]

    assert not second_teacher.check_homework(result_2)
    assert result_2 not in Teacher.homework_done[second_hw]

    Teacher.reset_results()
    assert not Teacher.homework_done
