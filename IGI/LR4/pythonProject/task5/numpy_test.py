import numpy as np


class NumpyTest:
    @staticmethod
    def test():
        """
        Showing numpy methods
        """
        lst = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
        array_np = np.array(lst)
        print("\nTesting numpy functions...")
        print("Creating array via numpy.array:")
        print(array_np)

        print("Slice of this array:")
        print(array_np[1:5])

        print("Array + 3:")
        array_np = np.add(array_np, 3)
        print(array_np)

        print("Array * -4:")
        array_np = np.multiply(array_np, -4)
        print(array_np)

        print("Array mean value:")
        print(np.mean(array_np))

        print("Array correlation coefficients:")
        print(np.corrcoef(array_np))

        print("Array dispersion:")
        print(np.var(array_np))

        print("Array RMS value:")
        print(f"{np.std(array_np):.5f}")
