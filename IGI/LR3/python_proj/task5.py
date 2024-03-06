from input_funcs import input_int, input_float
import random


def generate_float_numbers(num):
    for i in range(num):
        yield random.uniform(-1_000, 1_000)


def count_list_parameters():
    """
    Function count the max element to absolute value of the sequence\nand the sum of elements betwenn the 1st and 2nd negative elements 
    """
    print("Enter the list length:")
    list_len = input_int()
    lst = []
    print("Enter 1 to enter the numbers to list by keybord or 2 to generate list with random numbers:")
    q = input_int()

    if q == 1:
        for i in range(list_len):
            print("Enter the float number:")
            num = input_float()
            lst.append(num)
    else:
        for i in range(list_len):
            lst = [i for i in generate_float_numbers(list_len)]

    max_el = max(lst, key=lambda x: abs(x))
    
    sum_el = 0
    is_neg_first = False
    is_neg_second = False
    for i in lst:
        if i < 0 and is_neg_first == False:
            is_neg_first = True
            continue
        elif i < 0 and is_neg_first == True:
            is_neg_second = True
            break
        if is_neg_first == True:
            sum_el += i

    if is_neg_second == False:
        sum_el = 0

    return max_el, sum_el, lst    