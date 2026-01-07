import sqlite3
import hashlib

DB_NAME = "users.db"

def create_db():
    # створення таблиці users
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL
                )
            """)
            conn.commit()
            print("База даних створена.")
    except sqlite3.Error as e:
        print(f"Помилка при створенні БД: {e}")


def hash_password(password):

    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def add_user():
    # додавання користувача
    print("\n--- Реєстрація користувача ---")
    login = input("Введіть логін: ")
    password = input("Введіть пароль: ")
    full_name = input("Введіть ПІБ: ")

    hashed_pw = hash_password(password)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)",
                           (login, hashed_pw, full_name))
            conn.commit()
            print(f"Користувача '{login}' додано!")
    except sqlite3.IntegrityError:
        print("Користувач з таким логіном вже існує!")
    except sqlite3.Error as e:
        print(f"Помилка бази даних: {e}")


def update_password():
    # оновлення паролю
    print("\n--- Зміна паролю ---")
    login = input("Введіть логін користувача: ")
    new_password = input("Введіть новий пароль: ")

    new_hashed_pw = hash_password(new_password)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # перевірка користувача
            cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
            if cursor.fetchone() is None:
                print("Користувача не знайдено.")
                return

            cursor.execute("UPDATE users SET password = ? WHERE login = ?", (new_hashed_pw, login))
            conn.commit()
            print(f"Пароль для '{login}' оновлено.")
    except sqlite3.Error as e:
        print(f"Помилка бази даних: {e}")


def authenticate_user():
    # перевірка логіну та паролю
    print("\n--- Вхід у систему ---")
    login = input("Введіть логін: ")
    password = input("Введіть пароль: ")

    hashed_input_pw = hash_password(password)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT full_name FROM users WHERE login = ? AND password = ?",
                           (login, hashed_input_pw))
            user = cursor.fetchone()

            if user:
                print(f"Ласкаво просимо, {user[0]}.")
                return True
            else:
                print("Невірний логін або пароль.")
                return False
    except sqlite3.Error as e:
        print(f"Помилка бази даних: {e}")
        return False


def main():
    create_db()

    while True:
        print("\n=== Меню ===")
        print("1. Додати користувача")
        print("2. Змінити пароль")
        print("3. Увійти (Автентифікація)")
        print("4. Вихід")

        choice = input("Ваш вибір(1-4): ")

        if choice == '1':
            add_user()
        elif choice == '2':
            update_password()
        elif choice == '3':
            authenticate_user()
        elif choice == '4':
            print("До побачення!")
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")


if __name__ == "__main__":
    main()