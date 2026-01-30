"""Робота з CSV файлами"""

import pandas as pd

df = pd.read_csv("students.csv")

print(df.head())

df = pd.read_csv("students.csv")

average_grade = df["Оцінка"].mean()

print(f"Середня оцінка: {average_grade:.2f}")

df = pd.read_csv("students.csv")

new_student = {"Ім'я": "Віталій", "Вік": 44, "Оцінка": 100}

df = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)

df.to_csv("students.csv", index=False, encoding="utf-8")

print("Новий студент доданий у файл")
print(df.head())
