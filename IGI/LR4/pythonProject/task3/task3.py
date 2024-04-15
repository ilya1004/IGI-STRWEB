import numpy as np
from task3.plot_maker import PlotMaker
from task3.sequence_functions import SequenceFunctions

from services.input_funcs import Input


class Task3:
    def __init__(self):
        self.__sequence = np.array([])

    @property
    def sequence(self):
        return self.__sequence

    @sequence.setter
    def sequence(self, seq):
        self.__sequence = seq

    def solve(self):
        """
        Function for solving this task
        """
        summ, f_x, k, x, eps = self.count_row()
        print(f"Arithmetic mean: {SequenceFunctions.get_arth_mean(self.sequence):.5f}")
        print(f"Median: {SequenceFunctions.get_median(self.sequence):.5f}")
        print(f"Mode: {SequenceFunctions.get_mode(self.sequence)}")
        print(f"Variance: {SequenceFunctions.get_dispersion(self.sequence):.5f}")
        print(f"Sequence RMS: {SequenceFunctions.get_sko(self.sequence):.5f}")
        print(f"x\t\t n\t F(x)\t\t Math F(x)\t eps")
        print(f"{x:.3f}\t {k}\t {f_x:.7f}\t {summ:.7f}\t {eps}")
        PlotMaker.make_plot(-1, 1, 0.01, "task3_plot.png")

    def count_row(self):
        """
        Function for counting row with eps
        """
        while True:
            print("Enter x (|x| < 1):")
            x = Input.input_float()
            if abs(x) >= 1:
                print("Error. Value 'x' must be |x| < 1")
            else:
                break
        print("Enter eps:")
        eps = Input.input_float()

        summ, k = 0, 0
        f_x = 1/(1 - x)

        series_nums = np.array([])
        while True:
            summ += x ** k
            series_nums = np.append(series_nums, x ** k)
            if abs(summ - f_x) <= eps or k >= 500:
                break
            k += 1

        self.sequence = series_nums

        return summ, f_x, k, x, eps


