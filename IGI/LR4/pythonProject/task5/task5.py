import numpy as np
from services.input_funcs import Input
from task5.numpy_test import NumpyTest


class Task5:
    def __init__(self):
        self.matrix = None

    def solve(self):
        """
        Function for solving task
        """
        self.generate_matrix()

        last_row = np.sort(self.matrix[-1])
        print("Sorted last row of matrix:")
        print(*last_row)

        print(f"Median for this row via numpy: {np.median(last_row)}")
        print(f"Median for this row via custom functions: {np.median(last_row)}")

        NumpyTest.test()

    def count_median(self, lst):
        """
        Custom function for counting median
        """
        sorted_lst = sorted(lst)
        n = len(sorted_lst)
        if n % 2 == 0:
            return (sorted_lst[n // 2 - 1] + sorted_lst[n // 2]) / 2
        else:
            return sorted_lst[n // 2]

    def generate_matrix(self):
        """
        Function for generating matrix
        """
        print("Enter the rows number (n):")
        n = Input.input_int()
        print("Enter the cols number (m):")
        m = Input.input_int()
        self.matrix = np.random.randint(-1000, 1000, size=(n, m))

        print(self.matrix)
