
def is_valid_int(value):
    """
    Check the validity of the int number
    """
    try:
        int_value = int(value) 
        return str(int_value) == value
    except ValueError:
        return False
    except Exception:
        return False


def input_int():
    """
    Input valudation of int numbers
    """
    n = None
    while True:
        num = input()
        if is_valid_int(num):
            n = int(num)
            break
        else:
            print("Enter the incorrect number. Try again:")
    return n


def is_valid_float(value):
    """
    Check the validity of the float number
    """
    try:
        float_value = float(value)
        return True
    except ValueError:
        return False
    except Exception:
        return False


def input_float() -> float:
    """
    Input valudation of float numbers
    """
    n = None
    while True:
        num = input()
        if is_valid_float(num):
            n = float(num)
            break
        else:
            print("Enter the incorrect number. Try again:")
    return n