from PIL import ImageDraw, Image, ImageFont
from numpy import sin, cos, degrees, radians

from task4.figure_color import FigureColor
from task4.geometric_figure import GeometricFigure
from task4.utils import Utils


class Parallelogram(GeometricFigure, FigureColor):
    def __init__(self, a_side: float, b_side: float, angle: float, color: str, text=""):
        super().__init__(color)
        self.a_side = a_side
        self.b_side = b_side
        self.angle_degrees = angle
        self.color = FigureColor(color)
        self.__text = text
        self.image = Image.new("RGB", (1000, 1000), "white")

    def get_text(self):
        return self.__text

    def set_text(self, new_text):
        self.__text = new_text

    def del_text(self):
        del self.__text

    text = property(fget=get_text, fset=set_text, fdel=del_text, doc=f"This is the text on figure")

    def count_square(self):
        """
        Counts the square of parallelogram
        """
        return self.a_side * self.b_side * sin(radians(self.angle_degrees))

    def __str__(self):
        return ("Side A: {}, side B: {}, angle: {}, color: {}"
                .format(self.a_side, self.b_side, self.angle_degrees, self.color))

    def draw(self):
        """
        Function to draw figure
        """
        draw = ImageDraw.Draw(self.image)
        x, y = 200, 200
        vertices = [(x, y),
                    (x + self.a_side, y),
                    (x + self.a_side + self.b_side * cos(radians(self.angle_degrees)),
                     y + self.b_side * sin(radians(self.angle_degrees))),
                    (x + self.b_side * cos(radians(self.angle_degrees)),
                     y + self.b_side * sin(radians(self.angle_degrees)))]

        draw.polygon(vertices, fill=self.color.__str__())
        xc, yc = Utils.add(vertices[2], vertices[0])[0] / 2, Utils.add(vertices[2], vertices[0])[1] / 2
        font = ImageFont.truetype("arial.ttf", size=26)
        draw.text((xc - 40, yc), self.__text, font=font, fill='black')
        self.image.save("task4_img.jpg")
        self.image.show()
