class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        if self.width == self.height:
            return True
        else:
            return False

    def resize(self, new_width, new_height):
        self.width = new_width
        self.height = new_height

rect = Rectangle(5, 10)

print(f"Площадь прямоугольника: {rect.area()}")
print(f"Периметр прямоугольника: {rect.perimeter()}")
print(f"Это квадрат? {rect.is_square()}")

rect.resize(2, 2)

print(f"Новая ширина: {rect.width}")
print(f"Новая высота: {rect.height}")

print(f"Новая площадь прямоугольника: {rect.area()}")
print(f"Новый периметр прямоугольника: {rect.perimeter()}")
print(f"Это квадрат? {rect.is_square()}")
