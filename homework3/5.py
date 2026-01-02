"""For built-in functions implementation"""

class MyList:
    """Клас-обгортка для списку з підтримкою базових методів."""

    def __init__(self, data):
        """Ініціалізує об'єкт MyList з переданими даними."""
        self.data = data

    def __len__(self):
        """Повертає довжину списку."""
        return len(self.data)

    def __iter__(self):
        """Дозволяє ітеруватися по елементах."""
        yield from self.data

    def __getitem__(self, index):
        """Доступ до елемента за індексом."""
        return self.data[index]


# Власні функції
def my_len(container) -> int:
    """Повертає кількість елементів у контейнері."""
    return len(container)


def my_sum(container) -> int | float:
    """Обчислює суму елементів у контейнері."""
    total = 0
    for item in container:
        total += item
    return total


def my_min(container):
    """Повертає мінімальний елемент у контейнері."""
    iterator = iter(container)
    try:
        minimum = next(iterator)
    except StopIteration as exc:
        raise ValueError("my_min() arg є порожньою послідовністю") from exc

    for item in iterator:
        minimum = min(minimum, item)
    return minimum


def test_functions():
    """Тестує роботу власних функцій."""
    nums = MyList([3, 1, 4, 1, 5, 9])

    print("Тест my_len:", my_len(nums))
    print("Тест my_sum:", my_sum(nums))
    print("Тест my_min:", my_min(nums))

    empty = MyList([])
    print("Тест my_len (порожній):", my_len(empty))
    try:
        print("Тест my_min (порожній):", my_min(empty))
    except ValueError as e:
        print("Помилка my_min:", e)


if __name__ == "__main__":
    test_functions()
