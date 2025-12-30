"""Трекер витрат"""

total_expense: float = 0.0  #Чому Pylint вважає total_expense констанотою?

def add_expense(amount: float) -> None:
    """Функція, яка додає витрати до загальної суми (total_expense)"""
    global total_expense
    total_expense += amount

def get_expense() -> float:
    """Функція, яка повертає загальну суму витрат"""
    return total_expense

def main() -> None:
    """Консольний інтерфейс"""
    while True:
        print("\nМеню:")
        print("1. Додати витрату")
        print("2. Показати загальну суму витрат")
        print("3. Вихід")

        choice: str = input("Виберіть опцію: ")

        if choice == "1":
            try:
                amount: float = float(input("Введіть суму витрати: "))
                add_expense(amount)
                print("Витрату додано!")
            except ValueError:
                print("Помилка: введіть число.")
        elif choice == "2":
            print(f"Загальна сума витрат: {get_expense()} грн")
        elif choice == "3":
            print("Вихід з програми.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
