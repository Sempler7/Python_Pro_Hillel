"""to-Compare"""


class Person:
    """Клас для представлення людини з ім'ям та віком"""
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __lt__(self, other: "Person") -> bool:
        """Менше за віком"""
        if not isinstance(other, Person):
            return NotImplemented
        return self.age < other.age

    def __eq__(self, other: object) -> bool:
        """Рівні за віком"""
        if not isinstance(other, Person):
            return NotImplemented
        return self.age == other.age

    def __gt__(self, other: "Person") -> bool:
        """Більше за віком"""
        if not isinstance(other, Person):
            return NotImplemented
        return self.age > other.age

    def __repr__(self) -> str:
        return f"Person(name='{self.name}', age={self.age})"


people = [
    Person("Олексій", 25),
    Person("Марія", 30),
    Person("Іван", 20),
    Person("Наталя", 25)
]

sorted_people = sorted(people)
print(sorted_people)
