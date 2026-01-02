"""Программа для работы с прямоугольниками: вычисление площади, периметра и проверка на квадрат."""

class Rectangle:
    """Класс, представляющий прямоугольник."""

    def __init__(self, width: float, height: float) -> None:
        """Инициализирует прямоугольник с заданной шириной и высотой."""
        self.width = width
        self.height = height

    def area(self) -> float:
        """Возвращает площадь прямоугольника."""
        return self.width * self.height

    def perimeter(self) -> float:
        """Возвращает периметр прямоугольника."""
        return 2 * (self.width + self.height)

    def is_square(self) -> bool:
        """Проверяет, является ли прямоугольник квадратом."""
        return self.width == self.height

    def resize(self, new_width: float, new_height: float) -> None:
        """Изменяет размеры прямоугольника."""
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
