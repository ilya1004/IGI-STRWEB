
class Input:
    @staticmethod
    def __is_valid_int(value):
        """
        Check the validity of the int number
        """
        try:
            int_value = int(value)
            return str(int_value) == value
        except ValueError:
            return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def input_int():
        """
        Input validation of int numbers
        """
        n = None
        while True:
            num = input()
            if Input.__is_valid_int(num):
                n = int(num)
                break
            else:
                print("Enter the incorrect number. Try again:")
        return n

    @staticmethod
    def __is_valid_float(value):
        """
        Check the validity of the float number
        """
        try:
            _ = float(value)
            return True
        except ValueError:
            return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def input_float() -> float:
        """
        Input validation of float numbers
        """
        n = None
        while True:
            num = input()
            if Input.__is_valid_float(num):
                n = float(num)
                break
            else:
                print("Enter the incorrect number. Try again:")
        return n

    @staticmethod
    def input_float_conds(min_value, max_value):
        """
        Input and value validation of float numbers
        """
        n = None
        while True:
            num = input()
            if Input.__is_valid_float(num):
                n = float(num)
                if min_value <= n <= max_value:
                    break
                else:
                    print("Enter the incorrect value. Try again:")
            else:
                print("Enter the incorrect number. Try again:")
        return n

    @staticmethod
    def input_color():
        """
        Input validation of figure color
        """
        color = "red"
        while True:
            color = input()
            if color not in ["red", "green", "blue", "white", "cyan", "magenta", "yellow", "orange", "purple", "gray"]:
                print("Entered color not in colors list. Try again:")
            else:
                break
        return color
