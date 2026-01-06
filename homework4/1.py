"""Простий консольний калькулятор з обробкою винятків"""


class UnknownOperationError(Exception):
    """Власний виняток для невідомих операцій."""


def calculator(a: float, b: float, operation: str) -> float | None:
    """Простий калькулятор з обробкою винятків.
    """
    try:
        if operation == "+":
            return a + b
        if operation == "-":
            return a - b
        if operation == "*":
            return a * b
        if operation == "/":
            return a / b
        raise UnknownOperationError(f"Невідома операція: {operation}")
    except ZeroDivisionError:
        print("Помилка: ділення на нуль!")
    except OverflowError:
        print("Помилка: переповнення числа!")
    except Exception as e:
        print(f"Інша помилка: {e}")
    return None


def main() -> None:
    """Основна функція програми — консольний калькулятор.
    """
    while True:
        try:
            a: float = float(input("Введіть перше число: "))
            b: float = float(input("Введіть друге число: "))
            op: str = input("Введіть операцію (+, -, *, /): ")

            result: float | None = calculator(a, b, op)
            if result is not None:
                print(f"Результат: {result}")

        except ValueError:
            print("Помилка: потрібно вводити числа!")

        # Можливість завершити програму
        cont: str = input("Продовжити? (y/n): ").lower()
        if cont != "y":
            break


if __name__ == "__main__":
    main()
