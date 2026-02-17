"""Цей скрипт демонструє використання модуля multiprocessing
для обчислення суми великого масиву чисел.
"""

import multiprocessing as mp
import random
import time


def partial_sum(numbers: list[int]) -> int:
    """Функція для обчислення суми частини масиву."""
    return sum(numbers)


def main():
    """Головна функція для створення великого масиву чисел та обчислення його суми."""
    array_size = 1_000_000
    numbers = [random.randint(1, 100) for _ in range(array_size)]

    #  Визначаємо кількість процесів
    num_processes = mp.cpu_count()

    chunk_size = len(numbers) // num_processes
    chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]

    start_time = time.perf_counter()

    with mp.Pool(processes=num_processes) as pool:
        partial_results = pool.map(partial_sum, chunks)

    total_sum = sum(partial_results)

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    print(f"Кількість процесів: {num_processes}")
    print(f"Сума масиву: {total_sum}")
    print(f"Час виконання: {elapsed:.4f} секунд")


if __name__ == "__main__":
    main()
