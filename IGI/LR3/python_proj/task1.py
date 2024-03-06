
from input_funcs import input_float


def count_row():
    """
    Function for counting row with eps
    """    
    while True:
        print("Enter x:")
        x = input_float()
        if abs(x) >= 1:
            print("Error. Value 'x' must be |x| < 1")
        else:
            break
    print("Enter eps:")
    eps = input_float()

    sum, k = 0, 0
    f_x = 1/(1 - x)

    while True:
        sum += x ** k
        if abs(sum - f_x) <= eps or k >= 500:
            break
        k += 1
           
    return sum, f_x, k, x, eps
        