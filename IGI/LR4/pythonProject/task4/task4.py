from math import radians, degrees
from services.input_funcs import Input
from task4.parallelogram import Parallelogram


class Task4:
    def __init__(self):
        self.figure = None

    def solve(self):
        """
        Function for solving task
        """
        self.input_parallelogram()
        self.figure.draw()
        print(self.figure)
        print(f"Parallelogram square: {self.figure.count_square()}")

    def input_parallelogram(self):
        """
        Function for enter the parallelogram parameters
        """
        print("Drawing the parallelogram")
        print("Enter the side A:")
        a = Input.input_float_conds(0, 700)
        print("Enter the side B:")
        b = Input.input_float_conds(0, 700)
        print("Enter the angle (in degrees):")
        angle = degrees(radians(Input.input_float_conds(0, 180)))
        print("Choose the color from the list and write its name:")
        print('"red" (красный), "green" (зеленый), "blue" (синий), "white" (белый), "cyan" (голубой),'
              '"magenta" (пурпурный), "yellow" (желтый), "orange" (оранжевый), "purple" (фиолетовый), "gray" (серый)')
        color = Input.input_color()
        print("Enter the text to write it in figure:")
        txt = input()

        self.figure = Parallelogram(a, b, angle, color, txt)
