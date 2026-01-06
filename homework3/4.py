"""Binary"""


class BinaryNumber:
    """
    Клас для представлення невід’ємних цілих чисел у двійковій формі
    та виконання побітових операцій над ними.
    """
    def __init__(self, value: int):
        """Ініціалізує об’єкт BinaryNumber"""
        if value < 0:
            raise ValueError("BinaryNumber must be non-negative")
        self.value = value

    def __and__(self, other: "BinaryNumber") -> "BinaryNumber":
        """Побітове AND між двома двійковими числами"""
        return BinaryNumber(self.value & other.value)

    def __or__(self, other: "BinaryNumber") -> "BinaryNumber":
        """Побітове OR між двома двійковими числами"""
        return BinaryNumber(self.value | other.value)

    def __xor__(self, other: "BinaryNumber") -> "BinaryNumber":
        """Побітове XOR між двома двійковими числами"""
        return BinaryNumber(self.value ^ other.value)

    def __invert__(self) -> "BinaryNumber":
        """Побітове NOT (інверсія всіх бітів)"""
        return BinaryNumber(~self.value & 0xFF)

    def __repr__(self) -> str:
        """Текстове представлення об’єкта у вигляді двійкового рядка"""
        return f"{bin(self.value)}"


def test_binary_operations():
    """Демонстрація роботи класу BinaryNumber"""
    a = BinaryNumber(0b1010)  # 10 у двійковій формі: 1010
    b = BinaryNumber(0b1100)  # 12 у двійковій формі: 1100

    print("a =", a)  # 0b1010
    print("b =", b)  # 0b1100

    print("AND:", a & b)   # 0b1000 (8)
    print("OR:", a | b)    # 0b1110 (14)
    print("XOR:", a ^ b)   # 0b0110 (6)
    print("NOT a:", ~a)    # 0b11110101 (245 у 8-бітному представленні)


test_binary_operations()
