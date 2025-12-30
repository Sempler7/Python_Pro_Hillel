"""Програма - імітіція менеджера підписки на розсилку
"""

subscribers: list[str] = []

def subscribe(name: str) -> str:
    """Функція, яка додає ім'я підписника до списку імен (subscribers)"""
    subscribers.append(name)

    def confirm_subscription() -> str:
        """Вкладена функція, яка повертає повідомлення з підтвердженням підписки """
        return f"Підписка підтверджена для {name}"

    print(confirm_subscription())
    return name



def unsubscribe(name: str) -> str:
    """Функція, яка відаляє ім'я зі списку (subscribers) """
    if name in subscribers:
        subscribers.remove(name)
        return f"{name} успішно відписаний"
    return f"{name} не знайдено у списку підписників"

#  ще один варіант запису функції відписки

# def unsubscribe(name):
#     try:
#         subscribers.remove(name)
#         return f"{name} успішно відписаний"
#     except ValueError:
#         return f"{name} не знайдено у списку підписників"

subscribe("Vit")
subscribe("Вася")
subscribe("Kate")

print(subscribers)
print(unsubscribe("Вася"))
print(unsubscribe("Olena"))
print(subscribers)
