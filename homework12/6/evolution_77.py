"""Симуляція еволюції організмів з використанням multiprocessing та threading."""

import random
import multiprocessing
import threading
import os
from typing import List


class Organism:
    """Простий організм з енергією та віком"""

    def __init__(self, energy: int = 100, age: int = 0):
        self.energy = energy
        self.age = age

    def live(self):
        """Організм витрачає енергію та старіє"""
        self.energy -= random.randint(5, 15)
        self.age += 1

    def eat(self):
        """Організм отримує енергію з їжі"""
        self.energy += random.randint(10, 30)

    def reproduce(self) -> "Organism | None":
        """Розмноження можливе, якщо енергії достатньо"""
        if self.energy > 120:
            self.energy //= 2
            return Organism(energy=self.energy)
        return None

    def is_alive(self) -> bool:
        """Організм живий, якщо має енергію та не надто старий"""
        return self.energy > 0 and self.age < 50


def simulate_organism(org: Organism) -> List[Organism]:
    """Симуляція життя одного організму та його потомства"""
    offspring = []
    org.live()
    if random.random() < 0.5:  # ймовірність знайти їжу
        org.eat()
    child = org.reproduce()
    if child:
        offspring.append(child)
    return [org] + offspring if org.is_alive() else offspring


def simulate_population(population: List[Organism], use_processes: bool = True) -> List[Organism]:
    """Симуляція життя всієї популяції з використанням multiprocessing або threading"""
    max_workers = min(len(population), os.cpu_count() or 4)

    if use_processes:
        with multiprocessing.Pool(processes=max_workers) as pool:
            results = pool.map(simulate_organism, population)
    else:
        results = []
        threads = []
        output: List[List[Organism]] = [[] for _ in population]

        def worker(i, org):
            output[i] = simulate_organism(org)

        for i, org in enumerate(population):
            t = threading.Thread(target=worker, args=(i, org))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        results = output

    new_population = [org for sublist in results for org in sublist]
    return new_population


if __name__ == "__main__":
    population_start = [Organism() for _ in range(10)]
    for generation in range(5):  # можна збільшити кількість поколінь
        population_start = simulate_population(population_start, use_processes=True)
        print(f"Покоління {generation}: {len(population_start)} організмів")
