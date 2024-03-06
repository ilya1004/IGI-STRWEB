from input_funcs import input_float, input_int


def decorator_function(original_function):
    def wrapper(*args, **kwargs):
        print(f"Function {original_function.__name__} start its work")
        print("This function for counting sum of row until a negative number.")
        result = original_function(*args, **kwargs)
        print(f"Function {original_function.__name__} end its work")
        return result
    return wrapper


@decorator_function
def int_sum_intput_row():
    """
    Function for counting sum of row until a negative number
    """
    sum = 0
    while True:
        print("Enter the number to sum it:")
        num = input_int()
        if num < 0:
            break
        sum += num
    return sum
