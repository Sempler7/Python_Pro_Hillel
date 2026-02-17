"""Обчислення факторіала великого числа з використанням паралельних процесів"""

import math
import multiprocessing
from typing import Tuple


def partial_factorial(start: int, end: int) -> int:
    """
    Обчислює добуток чисел від start до end включно.
    """
    result = 1
    for i in range(start, end + 1):
        result *= i
    return result


def chunk_ranges(n: int, num_chunks: int) -> list[Tuple[int, int]]:
    """
    Розбиває діапазон [1, n] на num_chunks частин.
    """
    chunk_size = n // num_chunks
    ranges = []
    start = 1
    for i in range(num_chunks):
        end = start + chunk_size - 1
        if i == num_chunks - 1:  # останній шматок включає залишок
            end = n
        ranges.append((start, end))
        start = end + 1
    return ranges


def parallel_factorial(n: int, num_processes: int = 4) -> int:
    """
    Обчислює факторіал числа n паралельно.
    """
    ranges = chunk_ranges(n, num_processes)
    with multiprocessing.Pool(processes=num_processes) as pool:
        partial_results = pool.starmap(partial_factorial, ranges)
    # Об’єднуємо результати
    result = math.prod(partial_results)
    return result


if __name__ == "__main__":
    NUMBER = 100000  # велике число
    PROCESSES = 8  # кількість процесів
    print(f"Обчислення факторіалу {NUMBER} з використанням {PROCESSES} процесів...")
    factorial_value = parallel_factorial(NUMBER, PROCESSES)

    # Обчислюємо кількість цифр без перетворення у рядок
    num_digits = math.floor(math.log10(factorial_value)) + 1
    print(f"Факторіал {NUMBER} має {num_digits} цифр")
