"""Тестування з використанням doctest та покриття складних сценаріїв.
    Модуль для роботи з матрицями"""

from typing import List


def transpose_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Транспонує матрицю.

    >>> transpose_matrix([[1, 2], [3, 4]])
    [[1, 3], [2, 4]]

    >>> transpose_matrix([[1, 2, 3], [4, 5, 6]])
    [[1, 4], [2, 5], [3, 6]]

    >>> transpose_matrix([[7]])
    [[7]]

    >>> transpose_matrix([[1, 2], [3, 4], [5, 6]])
    [[1, 3, 5], [2, 4, 6]]
    """
    return [list(row) for row in zip(*matrix)]


def matrix_multiply(matrix1: List[List[int]], matrix2: List[List[int]]) -> List[List[int]]:
    """
    Множення двох матриць.

    >>> matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]

    >>> matrix_multiply([[2, 0], [0, 2]], [[1, 2], [3, 4]])
    [[2, 4], [6, 8]]

    >>> matrix_multiply([[1, 2, 3]], [[4], [5], [6]])
    [[32]]

    >>> matrix_multiply([[1, 0, 2], [-1, 3, 1]], [[3, 1], [2, 1], [1, 0]])
    [[5, 1], [4, 2]]
    """
    # Перевірка розмірностей
    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Кількість стовпців першої матриці має "
                         "дорівнювати кількості рядків другої.")

    result: List[List[int]] = []
    for row1 in matrix1:  # без i
        new_row: List[int] = []
        for col2 in zip(*matrix2):  # без j
            s = sum(a * b for a, b in zip(row1, col2))
            new_row.append(s)
        result.append(new_row)
    return result

#  Запуск тестів: python -m doctest -v matrix.py
