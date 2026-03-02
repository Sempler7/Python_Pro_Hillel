"""Скрипт для парсингу новин з сайту Укрінформ (https://www.ukrinform.ua/rubric-world)."""

from datetime import datetime, timedelta
from typing import Optional

import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd

# Словник українських місяців для нормалізації дат
MONTHS_UA = {
    "січня": "01", "лютого": "02", "березня": "03", "квітня": "04",
    "травня": "05", "червня": "06", "липня": "07", "серпня": "08",
    "вересня": "09", "жовтня": "10", "листопада": "11", "грудня": "12"
}


def get_page(url: str) -> Optional[BeautifulSoup]:
    """Завантажує HTML-код сторінки та повертає BeautifulSoup-об'єкт."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Помилка завантаження сторінки: {e}")
        return None


def parse_news(soup: BeautifulSoup) -> list[dict]:
    """Парсить новини зі сторінки Укрінформ."""
    news_list = []

    # Основні новини
    for article in soup.find_all("div", class_="news_item"):
        title_tag: Optional[Tag] = article.find("a", class_="title")
        link_tag: Optional[Tag] = article.find("a", href=True)
        date_tag: Optional[Tag] = article.find("span", class_="date")
        summary_tag: Optional[Tag] = article.find("p", class_="text")

        title = title_tag.get_text(strip=True) if title_tag else "N/A"
        link = ("https://www.ukrinform.ua" + link_tag["href"]  # type: ignore[operator]
                if (link_tag and link_tag.has_attr("href"))
                else "N/A")
        date = date_tag.get_text(strip=True) if date_tag else "N/A"
        summary = summary_tag.get_text(strip=True) if summary_tag else "N/A"

        news_list.append({"title": title, "link": link, "date": date, "summary": summary})

    # Блок "Останні новини"
    others = soup.find("aside", class_="others")
    if others:
        day_tag: Optional[Tag] = others.find("div", class_="othersDay")
        day_text = day_tag.get_text(strip=True) if day_tag else ""

        for item in others.find_all("a", href=True):
            if item.get_text(strip=True) == "Останні новини":
                continue
            time_tag: Optional[Tag] = item.find("span", class_="otherTime")
            time_text = time_tag.get_text(strip=True) if time_tag else ""
            date = f"{day_text} {time_text}".strip()
            link = ("https://www.ukrinform.ua" + item["href"]  # type: ignore[operator]
                    if item.has_attr("href")
                    else "N/A")
            news_list.append({
                "title": item.get_text(strip=True),
                "link": link,
                "date": date,
                "summary": item.get("title", "N/A")  # type: ignore[dict-item]
            })

    return news_list


def normalize_date(date_str: str) -> str:
    """Перетворює дату у формат YYYY-MM-DD HH:MM"""
    try:
        return datetime.strptime(date_str, "%d.%m.%Y %H:%M").strftime("%Y-%m-%d %H:%M")
    except ValueError:
        try:
            parts = date_str.split()
            if len(parts) >= 4:
                day, month, year, time = parts[0], parts[1], parts[2], parts[3]
                month_num = MONTHS_UA.get(month.lower(), "01")
                return f"{year}-{month_num}-{day.zfill(2)} {time}"
        except (IndexError, KeyError):
            pass
    return date_str


def clean_data(data: list[dict]) -> list[dict]:
    """Очищає дані від заглушок і нормалізує дати."""
    return [
        {**item, "date": normalize_date(item["date"])}
        for item in data
        if item["title"] != "Останні новини" and not all(v == "N/A" for v in item.values())
    ]


def save_to_csv(data: list[dict], filename: str = "news.csv") -> None:
    """Зберігає список новин у CSV-файл."""
    try:
        pd.DataFrame(data).to_csv(filename, index=False, encoding="utf-8")
        print(f"Дані збережено у файл {filename}")
    except (OSError, IOError) as e:
        print(f"Помилка збереження у CSV: {e}")


def filter_by_date(data: list[dict], days: int = 7) -> list[dict]:
    """Фільтрує новини за останні N днів."""
    cutoff = datetime.now() - timedelta(days=days)
    filtered = []
    for item in data:
        try:
            pub_date = datetime.strptime(item["date"], "%Y-%m-%d %H:%M")
            if pub_date >= cutoff:
                filtered.append(item)
        except ValueError:
            continue
    return filtered


if __name__ == "__main__":
    URL = "https://www.ukrinform.ua/rubric-world"
    some_soup = get_page(URL)
    if some_soup:
        news = parse_news(some_soup)
        print(f"Знайдено {len(news)} новин")
        news = clean_data(news)
        recent_news = filter_by_date(news, days=7)
        save_to_csv(recent_news, "news.csv")
