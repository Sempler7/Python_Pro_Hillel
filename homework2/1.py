"""Модуль, в якому ми використовуємо вбудовані функції та їх перекриття локальними функціями
"""
import builtins

def my_sum(*args: object, **kwargs: object) -> str:
    """Функція, яка просто виводить повідомлення"""
    return "This is my custom sum function!"

print(my_sum())

list_numbers: list[int] = [1,2,3,4,5]

print(sum(list_numbers))

sum = my_sum
sum(list_numbers)

print(builtins.sum(list_numbers))

