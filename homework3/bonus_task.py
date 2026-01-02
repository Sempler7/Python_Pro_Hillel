"""Модуль із дескриптором для конвертації валют."""


class CurrencyDescriptor:
    """Дескриптор для збереження ціни продукту з підтримкою USD та EUR"""
    def __init__(self, rate_usd=1.0, rate_eur=0.9):
        """Ініціалізує дескриптор із заданими курсами валют"""
        self._values = {}
        self.rate_usd = rate_usd
        self.rate_eur = rate_eur

    def __get__(self, instance, owner):
        """Повертає значення ціни для конкретного екземпляра класу"""
        if instance is None:
            return self
        value, currency = self._values.get(instance, (None, "USD"))
        if value is None:
            return "Ціна не встановлена"
        return f"{value:.2f} {currency}"

    def __set__(self, instance, value):
        """Встановлює значення ціни для екземпляра"""
        if isinstance(value, tuple):
            amount, currency = value
            if amount < 0:
                raise ValueError("Ціна не може бути від'ємною")
            if currency == "USD":
                self._values[instance] = (amount, "USD")
            elif currency == "EUR":
                usd_value = amount / self.rate_eur
                self._values[instance] = (usd_value, "USD")
            else:
                raise ValueError("Непідтримувана валюта")
        else:
            raise ValueError("Встановлюйте ціну як (сума, валюта)")


class ProductWithCurrency: # pylint: disable=too-few-public-methods
    """Клас продукту з ціною, що зберігається через дескриптор."""
    price = CurrencyDescriptor()

    def __init__(self, name: str, price: tuple):
        """Ініціалізує продукт із назвою та ціною"""
        self.name = name
        self.price = price

    def __repr__(self):
        """Повертає рядкове представлення продукту"""
        return f"ProductWithCurrency(name={self.name}, price={self.price})"


if __name__ == "__main__":
    p4 = ProductWithCurrency("Camera", (1000, "EUR"))
    print("Ціна в USD:", p4.price)
    p4.price = (1200, "USD")
    print("Ціна в USD:", p4.price)
