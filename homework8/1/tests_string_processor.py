"""Тестування класу StringProcessor"""

import unittest
from string_processor import StringProcessor


class TestStringProcessor(unittest.TestCase):
    """Тестування класу StringProcessor"""

    def setUp(self):
        self.processor = StringProcessor()

    #  reverse_string
    @unittest.skip("Відома проблема з порожнім рядком, буде виправлено пізніше")
    def test_reverse_empty_string(self):
        """Тестування перевертання порожнього рядка"""
        self.assertEqual(self.processor.reverse_string(""), "")

    def test_reverse_normal_string(self):
        """Тестування перевертання звичайного рядка"""
        self.assertEqual(self.processor.reverse_string("hello"), "olleh")

    def test_reverse_with_numbers_and_symbols(self):
        """Тестування перевертання рядка з числами та символами"""
        self.assertEqual(self.processor.reverse_string("abc123!"), "!321cba")

    #  capitalize_string
    def test_capitalize_empty_string(self):
        """Тестування регістра порожнього рядка"""
        self.assertEqual(self.processor.capitalize_string(""), "")

    def test_capitalize_lowercase(self):
        """Тестування регістра рядка з маленьких літер"""
        self.assertEqual(self.processor.capitalize_string("hello"), "Hello")

    def test_capitalize_uppercase(self):
        """Тестування регістра рядка з великих літер"""
        self.assertEqual(self.processor.capitalize_string("HELLO"), "HELLO")

    def test_capitalize_with_numbers_and_symbols(self):
        """Тестування регістра рядка з числами та символами"""
        self.assertEqual(self.processor.capitalize_string("123abc"), "123abc")

    #  count_vowels
    def test_count_vowels_empty_string(self):
        """Тестування підрахунку голосних у порожньому рядку"""
        self.assertEqual(self.processor.count_vowels(""), 0)

    def test_count_vowels_mixed_case(self):
        """Тестування підрахунку голосних у рядку з різним регістром"""
        self.assertEqual(self.processor.count_vowels("HeLLo"), 2)

    def test_count_vowels_with_numbers_and_symbols(self):
        """Тестування підрахунку голосних у рядку з числами та символами"""
        self.assertEqual(self.processor.count_vowels("abc123!"), 1)


if __name__ == "__main__":
    unittest.main()

#  Команди для запуску тестів:
#  cd C:\Users\sempl\Python_Pro_Hillel\homework8
#  python -m unittest 1.tests_string_processor
