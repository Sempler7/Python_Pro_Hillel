"""Робота з XML"""

import xml.etree.ElementTree as ET
from typing import Optional


def get_text(el: Optional[ET.Element], default: str = "") -> str:
    """Утиліта для безпечного отримання тексту з XML-елемента"""
    return el.text if el is not None and el.text is not None else default


tree = ET.parse("products.xml")
root = tree.getroot()

print("📦 Список продуктів:")
for product in root.findall("product"):
    name = get_text(product.find("name"))
    price = float(get_text(product.find("price"), "0"))
    quantity = int(get_text(product.find("quantity"), "0"))
    print(f"- {name}: {quantity} шт. (ціна {price} грн)")

for product in root.findall("product"):
    if get_text(product.find("name")) == "Шоколад":
        q_el = product.find("quantity")
        if q_el is not None:
            q_el.text = "10"  # нове значення

tree.write("products.xml", encoding="utf-8", xml_declaration=True)

print("\nКількість товару оновлено і файл збережено.")
