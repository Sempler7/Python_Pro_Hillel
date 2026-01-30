"""Тестування модуля file_processor.py за допомогою pytest"""

import pytest
from file_processor import FileProcessor


def test_file_write_read(tmpdir):
    """Тестування запису та читання з файлу."""
    file = tmpdir.join("testfile.txt")
    FileProcessor.write_to_file(file, "Hello, World!")
    content = FileProcessor.read_from_file(file)
    assert content == "Hello, World!"


def test_empty_string(tmpdir):
    """Тестування запису та читання порожнього рядка."""
    file = tmpdir.join("empty.txt")
    FileProcessor.write_to_file(file, "")
    content = FileProcessor.read_from_file(file)
    assert content == ""


def test_large_data(tmpdir):
    """Тестування запису та читання великого обсягу даних."""
    file = tmpdir.join("large.txt")
    large_text = "A" * 10 ** 6  # 1 мільйон символів
    FileProcessor.write_to_file(file, large_text)
    content = FileProcessor.read_from_file(file)
    assert content == large_text


def test_file_not_found():
    """Тестування читання з неіснуючого файлу."""
    with pytest.raises(FileNotFoundError):
        FileProcessor.read_from_file("non_existent.txt")
