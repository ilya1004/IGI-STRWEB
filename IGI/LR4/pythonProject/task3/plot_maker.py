import numpy as np
import matplotlib.pyplot as plt


class PlotMaker:
    @staticmethod
    def fx(x):
        return 1 / (1 - x)

    @staticmethod
    def count_row_item(x, eps):
        """
        Counts row to value x
        """
        summ, k = 0, 0
        f_x = 1/(1 - x)
        while True:
            summ += x ** k
            if abs(summ - f_x) <= eps or k >= 500:
                break
            k += 1
        return summ

    @staticmethod
    def make_plot(x_min, x_max, step, file_path):
        """
        Function for making plot of row
        """
        x_vals = np.arange(x_min, x_max, step)

        y_fx = [PlotMaker.fx(x) for x in x_vals]
        y_t = [PlotMaker.count_row_item(x, 0.1) for x in x_vals]

        plt.plot(x_vals, y_fx, color="blue")
        plt.plot(x_vals, y_t, color="red")

        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend(["1/(1-x) value", "taylor series value"])
        plt.annotate('Точка неопределенности', xy=(1, -0.3), xytext=(-0.2, 20),
                     arrowprops=dict(arrowstyle='->'))
        plt.title("Functions graphics")

        try:
            plt.savefig(file_path)
        except Exception as e:
            print(e)

        plt.show()
