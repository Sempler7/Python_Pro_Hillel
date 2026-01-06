"""Програма для зчитування чисел з текстового файлу"""

from typing import Optional


def calculate_average(file_path: str) -> Optional[float]:
    """Обчислює середнє арифметичне чисел із текстового файлу"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

            if not lines:
                raise ValueError("Файл порожній, неможливо обчислити середнє.")

            numbers = []
            for line in lines:
                line = line.strip()
                if line:
                    try:
                        numbers.append(float(line))
                    except ValueError as exc:
                        raise ValueError(f"Нечислові дані у файлі: '{line}'") from exc

            if not numbers:
                raise ValueError("Файл не містить жодного числа.")

            if len(numbers) == 1:
                print("У файлі лише одне число, середнє дорівнює самому числу.")
                return numbers[0]

            return sum(numbers) / len(numbers)

    except FileNotFoundError:
        print(f"Помилка: файл '{file_path}' не знайдено.")
        return None
    except ValueError as e:
        print(f"Помилка: {e}")
        return None


if __name__ == "__main__":
    result = calculate_average("numbers.txt")
    if result is not None:
        print(f"Середнє арифметичне: {result}")
