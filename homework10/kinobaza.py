"""консольний застосунок для керування базою даних "Кінобаза"""

import sqlite3
import datetime

DB_NAME = "kinobaza.db"


def connect_db():
    """Підключення до бази даних та налаштування користувацьких функцій"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")

    conn.create_function("movie_age", 1, movie_age)
    conn.create_function("actor_age", 1, actor_age)
    return conn


#  Користувацькі функції
def movie_age(year: int) -> int:
    """Функція, яка обчислює, скільки років минуло з моменту виходу фільму"""
    current_year = datetime.datetime.now().year
    return current_year - year


def actor_age(birth_year: int) -> int:
    """Функція, яка обчислює вік актора на основі його року народження"""
    current_year = datetime.datetime.now().year
    return current_year - birth_year


def init_db():
    """Ініціалізація бази даних та створення таблиць, якщо їх ще немає"""
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
    """Додавання фільму та його акторів"""
    conn = connect_db()
    cursor = conn.cursor()
    title = input("Назва фільму: ")
    year = int(input("Рік випуску: "))
    genre = input("Жанр: ")
    cursor.execute(
        "INSERT INTO movies (title, release_year, genre) VALUES (?, ?, ?)",
        (title, year, genre)
    )

    movie_id = cursor.lastrowid

    cursor.execute("SELECT id, name FROM actors")
    actors = cursor.fetchall()
    if actors:
        print("Доступні актори:")
        for actor_id, name in actors:
            print(f"{actor_id}. {name}")
    else:
        print("У базі ще немає акторів. Додайте їх через пункт меню 2.")

    actor_ids = input("Введіть ID акторів через кому (наприклад 1,2,3): ")
    if actor_ids.strip():
        for actor_id in actor_ids.split(","):
            actor_id = actor_id.strip()
            if actor_id.isdigit():
                cursor.execute(
                    "INSERT OR IGNORE INTO movie_cast (movie_id, actor_id) VALUES (?, ?)",
                    (movie_id, int(actor_id))
                )

    conn.commit()
    conn.close()
    print(f"Фільм '{title}' додано успішно")


def add_actor():
    """Додавання актора"""
    conn = connect_db()
    cursor = conn.cursor()
    name = input("Ім'я актора: ")
    birth_year = int(input("Рік народження: "))
    cursor.execute("INSERT INTO actors (name, birth_year) VALUES (?, ?)", (name, birth_year))
    conn.commit()
    conn.close()


def show_movies_with_actors():
    """Показати всі фільми з акторами"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.title, a.name
        FROM movies m
        INNER JOIN movie_cast mc ON m.id = mc.movie_id
        INNER JOIN actors a ON mc.actor_id = a.id
    """)
    rows = cursor.fetchall()
    movies = {}
    for title, actor in rows:
        movies.setdefault(title, []).append(actor)
    for i, (title, actors) in enumerate(movies.items(), 1):
        print(f"{i}. Фільм: {title}, Актори: {', '.join(actors)}")
    conn.close()


def show_unique_genres():
    """Показати всі унікальні жанри"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT genre FROM movies")
    for i, (genre,) in enumerate(cursor.fetchall(), 1):
        print(f"{i}. {genre}")
    conn.close()


def count_movies_by_genre():
    """Показати кількість фільмів за жанром"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT genre, COUNT(*) FROM movies GROUP BY genre")
    for genre, count in cursor.fetchall():
        print(f"{genre}: {count}")
    conn.close()


def avg_birth_year_by_genre():
    """Показати середній рік народження акторів у фільмах певного жанру"""
    conn = connect_db()
    cursor = conn.cursor()
    genre = input("Введіть жанр: ")
    cursor.execute("""
        SELECT AVG(a.birth_year)
        FROM actors a
        INNER JOIN movie_cast mc ON a.id = mc.actor_id
        INNER JOIN movies m ON mc.movie_id = m.id
        WHERE m.genre = ?
    """, (genre,))
    avg_year = cursor.fetchone()[0]
    print(f"Середній рік народження акторів у жанрі '{genre}': {avg_year:.2f}")
    conn.close()


def search_movie():
    """Пошук фільму за назвою (часткове співпадіння)"""
    conn = connect_db()
    cursor = conn.cursor()
    keyword = input("Введіть ключове слово: ")
    cursor.execute("SELECT title, release_year FROM movies WHERE title LIKE ?", (f"%{keyword}%",))
    for i, (title, year) in enumerate(cursor.fetchall(), 1):
        print(f"{i}. {title} ({year})")
    conn.close()


def paginate_movies():
    """Показати фільми з пагінацією"""
    conn = connect_db()
    cursor = conn.cursor()
    page = int(input("Номер сторінки: "))
    per_page = int(input("Кількість фільмів на сторінку: "))
    offset = (page - 1) * per_page
    cursor.execute("SELECT title FROM movies LIMIT ? OFFSET ?", (per_page, offset))
    for i, (title,) in enumerate(cursor.fetchall(), 1):
        print(f"{i}. {title}")
    conn.close()


def union_actors_movies():
    """Показати імена всіх акторів та назви всіх фільмів (UNION)"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM actors UNION SELECT title FROM movies")
    for i, (item,) in enumerate(cursor.fetchall(), 1):
        print(f"{i}. {item}")
    conn.close()


def show_movies_with_age():
    """Показати фільми та їхній вік (використання користувацької функції)"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT title, movie_age(release_year) FROM movies")
    for i, (title, age) in enumerate(cursor.fetchall(), 1):
        print(f"{i}. Фільм: {title} — {age} років")
    conn.close()


def show_all_actors():
    """Показати імена всіх акторів та їхній рік народження"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, birth_year FROM actors")
    rows = cursor.fetchall()
    if not rows:
        print("Акторів ще немає у базі.")
    else:
        for actor_id, name, birth_year in rows:
            print(f"{actor_id}. {name} (нар. {birth_year})")
    conn.close()


def show_all_movies():
    """Показати назви всіх фільмів, їхній рік випуску та жанр"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, release_year, genre FROM movies")
    rows = cursor.fetchall()
    if not rows:
        print("Фільмів ще немає у базі.")
    else:
        for movie_id, title, year, genre in rows:
            print(f"{movie_id}. {title} ({year}), жанр: {genre}")
    conn.close()


def edit_movie():
    """Редагування фільму за ID"""
    conn = connect_db()
    cursor = conn.cursor()
    show_all_movies()  # показати список фільмів з id
    movie_id = int(input("Введіть ID фільму, який хочете змінити: "))

    # перевірка чи існує фільм
    cursor.execute("SELECT id, title, release_year, genre FROM movies WHERE id = ?", (movie_id,))
    movie = cursor.fetchone()
    if not movie:
        print("Фільм з таким ID не знайдено.")
        conn.close()
        return

    print(f"Редагування фільму: {movie[1]} ({movie[2]}), жанр: {movie[3]}")
    new_title = input("Нова назва (Enter щоб залишити): ") or movie[1]
    new_year = input("Новий рік випуску (Enter щоб залишити): ") or movie[2]
    new_genre = input("Новий жанр (Enter щоб залишити): ") or movie[3]

    cursor.execute("UPDATE movies SET title=?, release_year=?, genre=? WHERE id=?",
                   (new_title, int(new_year), new_genre, movie_id))
    conn.commit()
    conn.close()
    print("Фільм оновлено")


def edit_actor():
    """Редагування актора за ID"""""
    conn = connect_db()
    cursor = conn.cursor()
    show_all_actors()  # показати список акторів з id
    actor_id = int(input("Введіть ID актора, якого хочете змінити: "))

    cursor.execute("SELECT id, name, birth_year FROM actors WHERE id = ?", (actor_id,))
    actor = cursor.fetchone()
    if not actor:
        print("Актор з таким ID не знайдено.")
        conn.close()
        return

    print(f"Редагування актора: {actor[1]} (нар. {actor[2]})")
    new_name = input("Нове ім'я (Enter щоб залишити): ") or actor[1]
    new_birth_year = input("Новий рік народження (Enter щоб залишити): ") or actor[2]

    cursor.execute("UPDATE actors SET name=?, birth_year=? WHERE id=?",
                   (new_name, int(new_birth_year), actor_id))
    conn.commit()
    conn.close()
    print("Актор оновлений")


def show_actors_with_age():
    """Показати імена всіх акторів та їхній вік (використання користувацької функції)"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, actor_age(birth_year) FROM actors")
    rows = cursor.fetchall()
    if not rows:
        print("Акторів ще немає.")
    else:
        for name, age in rows:
            print(f"Актор: {name} — {age} років")
    conn.close()


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
