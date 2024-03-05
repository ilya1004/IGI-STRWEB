import circle
import square

a = int(input("Enter the radius 'r' to circle:\n"))
print(f"Area of circle: {circle.area(a)}\nPerimeter of circle: {circle.perimeter(a)}\n")

b = int(input("Enter the side 'a' to square:\n"))
print(f"Area of square: {square.area(b)}\nPerimeter of square: {square.perimeter(b)}\n")