from task1.task1 import Task1
from task2.task2 import Task2
from task3.task3 import Task3
from task4.task4 import Task4
from task5.task5 import Task5
from services.input_funcs import Input

"""
Laboratory work №4 <<Working with files, classes, serializers, regular expressions and standard libraries.>>
Rabets I.O.
15.03.2024
"""


if __name__ == "__main__":
    while True:
        print("-" * 50)
        print("Enter the task number to run it or -1 to exit:")
        print("-" * 50)
        num = Input.input_int()
        if num == 1:
            task1 = Task1()
            task1.solve()
        elif num == 2:
            task2 = Task2()
            task2.solve()
        elif num == 3:
            task3 = Task3()
            task3.solve()
        elif num == 4:
            task4 = Task4()
            task4.solve()
        elif num == 5:
            task5 = Task5()
            task5.solve()
        elif num == -1:
            exit()
