from task1 import count_row
from task2 import int_sum_intput_row
from task3 import count_symbols_in_string
from task4 import count_parameters_of_text
from task5 import count_list_parameters
from input_funcs import input_int

"""
This program is created to pass the laboratoty work
Laboratory work №3 <<Standard data types, collections, functions, modules>>
Rabets I.O.
06.03.2024
"""


while True:
    print("-" * 50)
    print("Enter the task number to run it or '-1' to exit:")
    print("-" * 50)
    num = input_int()
    if num == 1:
        lst = list(count_row())
        print(f"x\t n\t F(x)\t\t Math F(x)\t eps")
        print(f"{lst[3]}\t {lst[2]}\t {lst[1]:.7f}\t {lst[0]:.7f}\t {lst[4]}")
    elif num == 2:
        res = int_sum_intput_row()
        print(f"Sum of the input numbers are {res}")
    elif num == 3:
        res = count_symbols_in_string()
        print(f"Number of symbols int string between 'f' and 'y' is {res}")
    elif num == 4:
        res = list(count_parameters_of_text())
        print(f"Number of words in text is {res[0]}")
        print(f"Number of repetitions of each letter in text:")
        for i in res[1]:
            print(f"{i}: {res[1][i]}")
        print(f"All phrases between commas in alpabetical order:")
        for i in res[2]:
            print(i)
    elif num == 5:
        res = count_list_parameters()
        print("Elements in list:")
        print(*res[2])
        print(f"Max element to absolute number is {res[0]}")
        print(f"Sum of elements between the 1st and the 2nd negative numbers is {res[1]}")
    elif num == -1:
        exit()
