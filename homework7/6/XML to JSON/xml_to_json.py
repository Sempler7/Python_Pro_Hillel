"""Перетворення XML у JSON"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict


def xml_to_dict(element: ET.Element) -> Dict[str, Any]:
    """Рекурсивно перетворює XML-елемент у словник."""
    node: Dict[str, Any] = {}

    if element.attrib:
        node["@attributes"] = element.attrib

    children = list(element)
    if children:
        child_dict: Dict[str, Any] = {}  # 🔑 ось тут правильна анотація
        for child in children:
            child_data = xml_to_dict(child)
            if child.tag in child_dict:
                if not isinstance(child_dict[child.tag], list):
                    child_dict[child.tag] = [child_dict[child.tag]]
                child_dict[child.tag].append(child_data[child.tag])
            else:
                child_dict.update(child_data)
        node[element.tag] = child_dict
    else:
        node[element.tag] = element.text.strip() if element.text else None

    return node


def xml_to_json(xml_file: str, json_file: str) -> None:
    """Перетворює XML-файл у JSON."""
    if not Path(xml_file).exists():
        raise FileNotFoundError(f"Файл {xml_file} не знайдено.")

    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = xml_to_dict(root)

    with open(json_file, mode="w", encoding="utf-8") as f_json:
        json.dump(data, f_json, ensure_ascii=False, indent=4)


# Використання
xml_to_json("products.xml", "XML to JSON/products.json")
