"""Імпортуй функції з модулів"""

from math_utils import factorial, gcd
from string_utils import upper_case, del_spaces


def main():
    """Демонстрація роботи імпортованих модулей"""
    print("Факторіал 5:", factorial(5))
    print("НСД(48, 18):", gcd(48, 18))

    text = "   Привіт, світ!   "
    print("Верхній регістр:", upper_case(text))
    print("Очищений рядок:", del_spaces(text))


if __name__ == "__main__":
    main()
