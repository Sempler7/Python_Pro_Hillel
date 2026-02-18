"""Паралельна обробка зображень: зміна розміру та застосування фільтра EMBOSS."""

from concurrent.futures import ProcessPoolExecutor
import pathlib
from PIL import Image, ImageFilter, UnidentifiedImageError


def process_image(image_path: str, output_dir: str) -> str:
    """Обробляє зображення: змінює розмір та застосовує фільтр EMBOSS"""
    try:
        img: Image.Image = Image.open(image_path)
        img = img.resize((300, 300))
        img = img.filter(ImageFilter.BLUR)

        output_path = pathlib.Path(output_dir) / f"processed_{pathlib.Path(image_path).name}"
        img.save(output_path)
        return str(output_path)

    except FileNotFoundError:
        return f"Файл не знайдено: {image_path}"
    except UnidentifiedImageError:
        return f"Неможливо відкрити зображення: {image_path}"
    except OSError as e:
        return f"Помилка при роботі з файлом {image_path}: {e}"


def main():
    """Головна функція для паралельної обробки зображень."""
    input_dir = "images"
    output_dir = "processed"
    pathlib.Path(output_dir).mkdir(exist_ok=True)

    image_files = list(pathlib.Path(input_dir).glob("*.jpg"))

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_image, str(img), output_dir) for img in image_files]

        for future in futures:
            print(future.result())


if __name__ == "__main__":
    main()
