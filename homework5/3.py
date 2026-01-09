""" Інспекція модулів на прикладі datetime"""

import importlib
import inspect


def analyze_module(module_name: str) -> None:
    """Аналізує модуль за назвою: виводить усі функції та класи з їхніми сигнатурами
    """
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        print(f"Модуль '{module_name}' не знайдено.")
        return

    functions = inspect.getmembers(module, inspect.isfunction)
    classes = inspect.getmembers(module, inspect.isclass)

    print("Функції:\n")
    if functions:
        for name, func in functions:
            try:
                sig = inspect.signature(func)
                print(f"- {name}{sig}")
            except (ValueError, TypeError):
                print(f"- {name}(...)")
    else:
        print("- <немає функцій у модулі>")

    print("\nКласи:\n")
    if classes:
        for name, _ in classes:
            print(f"- {name}")
    else:
        print("- <немає класів у модулі>")


# Приклад виконання
analyze_module("datetime")
