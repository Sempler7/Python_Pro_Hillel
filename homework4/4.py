"""Механізм для обробки ситуацій, коли гравцю не
вистачає ресурсів для виконання дій
"""


class InsufficientResourcesException(Exception):  # pylint: disable=too-few-public-methods
    """Клас винятку, що сигналізує про брак ресурсів у гравця для виконання дії"""

    def __init__(self, required_resource: str, required_amount: int, current_amount: int):
        """Ініціалізація винятка з інформацією про необхідний та наявний ресурс"""
        self.required_resource = required_resource
        self.required_amount = required_amount
        self.current_amount = current_amount
        super().__init__(self._generate_message())

    def _generate_message(self) -> str:
        """Формує повідомлення про брак ресурсу"""
        return (f"Недостатньо ресурсу '{self.required_resource}'. "
                f"Потрібно: {self.required_amount}, "
                f"маєте: {self.current_amount}.")


class Player:  # pylint: disable=too-few-public-methods
    """Клас, який представляє гравця з певними ресурсами"""

    def __init__(self, gold: int, mana: int):
        """Ініціалізує гравця з початковими ресурсами"""
        self.gold = gold
        self.mana = mana

    def perform_action(self, resource: str, cost: int):
        """Виконує дію, що потребує певного ресурсу"""
        current_amount = getattr(self, resource, None)
        if current_amount is None:
            raise ValueError(f"Ресурс '{resource}' не існує.")

        if current_amount < cost:
            raise InsufficientResourcesException(resource, cost, current_amount)

        setattr(self, resource, current_amount - cost)
        print(f"Дія виконана! Використано {cost} {resource}. Залишилось: {getattr(self, resource)}")


player = Player(gold=50, mana=10)

try:
    player.perform_action("gold", 100)  # Спроба витратити більше золота, ніж є
except InsufficientResourcesException as e:
    print(e)

try:
    player.perform_action("mana", 5)  # Достатньо мани
except InsufficientResourcesException as e:
    print(e)
