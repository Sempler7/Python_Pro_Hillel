"""консольний застосунок для керування базою даних "Кінобаза"""

import sqlite3
import datetime

DB_NAME = "kinobaza.db"


# Користувацькі функції
def movie_age(year: int) -> int:
    """Повертає вік фільму на основі року випуску."""
    return datetime.datetime.now().year - year


def actor_age(birth_year: int) -> int:
    """Повертає вік актора на основі року народження."""
    return datetime.datetime.now().year - birth_year


def connect_db():
    """Підключається до бази даних та налаштовує користувацькі функції."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.create_function("movie_age", 1, movie_age)
    conn.create_function("actor_age", 1, actor_age)
    return conn


def run_query(sql: str, params: tuple = (), fetch: bool = True):
    """Виконує SQL-запит з параметрами та повертає результат, якщо потрібно."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return result


def print_rows(rows, formatter, empty_message="Немає даних"):
    """Допоміжна функція для виведення рядків у відформатованому вигляді."""
    if not rows:
        print(empty_message)
    else:
        for row in rows:
            print(formatter(row))


#  Ініціалізація БД
def init_db():
    """Створює таблиці, якщо їх ще немає."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        release_year INTEGER NOT NULL,
        genre TEXT NOT NULL
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS actors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        birth_year INTEGER NOT NULL
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS movie_cast (
        movie_id INTEGER,
        actor_id INTEGER,
        PRIMARY KEY (movie_id, actor_id),
        FOREIGN KEY (movie_id) REFERENCES movies(id),
        FOREIGN KEY (actor_id) REFERENCES actors(id)
    )""")
    conn.commit()
    conn.close()


def add_movie():
    """Додає фільм та його акторів до бази даних."""
    title = input("Назва фільму: ")
    year = int(input("Рік випуску: "))
    genre = input("Жанр: ")
    run_query("INSERT INTO movies (title, release_year, genre) VALUES (?, ?, ?)",
              (title, year, genre), fetch=False)
    movie_id = run_query("SELECT last_insert_rowid()")[0][0]

    actors = run_query("SELECT id, name FROM actors")
    if actors:
        print("Доступні актори:")
        for actor_id, name in actors:
            print(f"{actor_id}. {name}")
    else:
        print("У базі ще немає акторів.")

    actor_ids = input("Введіть ID акторів через кому: ")
    if actor_ids.strip():
        for actor_id in actor_ids.split(","):
            actor_id = actor_id.strip()
            if actor_id.isdigit():
                run_query("INSERT OR IGNORE INTO movie_cast (movie_id, actor_id) VALUES (?, ?)",
                          (movie_id, int(actor_id)), fetch=False)
    print(f"Фільм '{title}' додано")


def add_actor():
    """Додає актора до бази даних."""
    name = input("Ім'я актора: ")
    birth_year = int(input("Рік народження: "))
    run_query("INSERT INTO actors (name, birth_year) VALUES (?, ?)",
              (name, birth_year), fetch=False)
    print(f"Актор '{name}' доданий")


def show_movies_with_actors():
    """Показує всі фільми з їхніми акторами."""
    rows = run_query("""SELECT m.title, a.name
                        FROM movies m
                        INNER JOIN movie_cast mc ON m.id = mc.movie_id
                        INNER JOIN actors a ON mc.actor_id = a.id""")
    movies = {}
    for title, actor in rows:
        movies.setdefault(title, []).append(actor)
    if not movies:
        print("Фільмів з акторами ще немає.")
    else:
        for i, (title, actors) in enumerate(movies.items(), 1):
            print(f"{i}. Фільм: {title}, Актори: {', '.join(actors)}")


def show_unique_genres():
    """Показує унікальні жанри фільмів."""
    rows = run_query("SELECT DISTINCT genre FROM movies")
    print_rows(rows, lambda r: f"{r[0]}", "Жанрів ще немає.")


def count_movies_by_genre():
    """Показує кількість фільмів за кожним жанром."""
    rows = run_query("SELECT genre, COUNT(*) FROM movies GROUP BY genre")
    print_rows(rows, lambda r: f"{r[0]}: {r[1]}", "Фільмів ще немає.")


def avg_birth_year_by_genre():
    """Показує середній рік народження акторів у вказаному жанрі."""
    genre = input("Введіть жанр: ")
    rows = run_query("""SELECT AVG(a.birth_year)
                        FROM actors a
                        INNER JOIN movie_cast mc ON a.id = mc.actor_id
                        INNER JOIN movies m ON mc.movie_id = m.id
                        WHERE m.genre = ?""", (genre,))
    avg_year = rows[0][0]
    if avg_year:
        print(f"Середній рік народження акторів у жанрі '{genre}': {avg_year:.2f}")
    else:
        print("Немає даних для цього жанру.")


def search_movie():
    """Пошук фільму за назвою (часткове співпадіння)."""
    keyword = input("Введіть ключове слово: ")
    rows = run_query("SELECT title, release_year FROM movies WHERE title LIKE ?", (f"%{keyword}%",))
    print_rows(rows, lambda r: f"{r[0]} ({r[1]})", "Фільмів не знайдено.")


def paginate_movies():
    """Показує фільми з пагінацією."""
    page = int(input("Номер сторінки: "))
    per_page = int(input("Кількість фільмів на сторінку: "))
    offset = (page - 1) * per_page
    rows = run_query("SELECT title FROM movies LIMIT ? OFFSET ?", (per_page, offset))
    print_rows(rows, lambda r: f"{r[0]}", "Фільмів ще немає.")


def union_actors_movies():
    """Показує імена акторів та назви фільмів в одному списку (UNION)."""
    rows = run_query("SELECT name FROM actors UNION SELECT title FROM movies")
    print_rows(rows, lambda r: f"{r[0]}", "База порожня.")


def show_movies_with_age():
    """Показує фільми та їхній вік, використовуючи користувацьку функцію movie_age."""
    rows = run_query("SELECT title, movie_age(release_year) FROM movies")
    print_rows(rows, lambda r: f"Фільм: {r[0]} — {r[1]} років", "Фільмів ще немає.")


def show_all_actors():
    """Показує всіх акторів з їхніми роками народження."""
    rows = run_query("SELECT id, name, birth_year FROM actors")
    print_rows(rows, lambda r: f"{r[0]}. {r[1]} (нар. {r[2]})", "Акторів ще немає.")


def show_all_movies():
    """Показує всі фільми з їхніми роками випуску та жанрами."""
    rows = run_query("SELECT id, title, release_year, genre FROM movies")
    print_rows(rows, lambda r: f"{r[0]}. {r[1]} ({r[2]}), жанр: {r[3]}", "Фільмів ще немає.")


def edit_movie():
    """Редагує інформацію про фільм."""
    show_all_movies()
    movie_id = int(input("Введіть ID фільму: "))
    rows = run_query("SELECT id, title, release_year, genre FROM movies WHERE id = ?", (movie_id,))
    if not rows:
        print("Фільм не знайдено.")
        return
    movie = rows[0]
    new_title = input("Нова назва (Enter щоб залишити): ") or movie[1]
    new_year = input("Новий рік випуску (Enter щоб залишити): ") or movie[2]
    new_genre = input("Новий жанр (Enter щоб залишити): ") or movie[3]
    run_query("UPDATE movies SET title=?, release_year=?, genre=? WHERE id=?",
              (new_title, int(new_year), new_genre, movie_id), fetch=False)
    print("Фільм оновлено ✅")


def edit_actor():
    """Редагує інформацію про актора."""
    show_all_actors()
    actor_id = int(input("Введіть ID актора: "))
    rows = run_query("SELECT id, name, birth_year FROM actors WHERE id = ?", (actor_id,))
    if not rows:
        print("Актор не знайдено.")
        return
    actor = rows[0]
    new_name = input("Нове ім'я (Enter щоб залишити): ") or actor[1]
    new_birth_year = input("Новий рік народження (Enter щоб залишити): ") or actor[2]
    run_query("UPDATE actors SET name=?, birth_year=? WHERE id=?",
              (new_name, int(new_birth_year), actor_id), fetch=False)
    print("Актор оновлений ✅")


def show_actors_with_age():
    """Показує акторів та їхній вік, використовуючи користувацьку функцію actor_age."""
    rows = run_query("SELECT name, actor_age(birth_year) FROM actors")
    print_rows(rows, lambda r: f"Актор: {r[0]} — {r[1]} років", "Акторів ще немає.")


def main():
    """Головна функція, яка запускає консольний застосунок"""
    init_db()
    actions = {
        "1": add_movie,
        "2": add_actor,
        "3": show_movies_with_actors,
        "4": show_unique_genres,
        "5": count_movies_by_genre,
        "6": avg_birth_year_by_genre,
        "7": search_movie,
        "8": paginate_movies,
        "9": union_actors_movies,
        "10": show_movies_with_age,
        "11": show_all_actors,
        "12": show_all_movies,
        "13": edit_movie,
        "14": edit_actor,
        "15": show_actors_with_age,
    }

    while True:
        print("""
1. Додати фільм
2. Додати актора
3. Показати всі фільми з акторами
4. Показати унікальні жанри
5. Показати кількість фільмів за жанром
6. Середній рік народження акторів у жанрі
7. Пошук фільму за назвою
8. Показати фільми (з пагінацією)
9. Імена акторів та назви фільмів
10. Фільми та їхній вік
11. Показати всіх акторів
12. Показати всі фільми
13. Редагувати фільм
14. Редагувати актора
15. Показати акторів та їхній вік
0. Вихід
        """)
        choice = input("Виберіть дію: ")
        if choice == "0":
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Невірний вибір!")


if __name__ == "__main__":
    main()
