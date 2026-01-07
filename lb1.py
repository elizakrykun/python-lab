import hashlib

# база даних користувачів
users_db = {}

def get_password_hash(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def register():
    print("\n--- Реєстрація нового коритувача ---")
    login = input("Придумайте логін: ").strip()

    # перевірка логіну
    if login in users_db:
        print(f"Помилка: Користувач '{login}' вже існує!")
        return

    password = input("Придумайте пароль: ")
    full_name = input("Введіть ваше ПІБ: ")

    # збереження
    users_db[login] = {
        'hash': get_password_hash(password),
        'full_name': full_name
    }
    print(f"Користувача {login} додано.")


def login():
    print("\n--- Вхід в систему ---")
    login = input("Логін: ").strip()
    password = input("Пароль: ")

    # перевірка наявності логіна
    if login not in users_db:
        print("Помилка: Користувача не знайдено.")
        return

    # перевірка пароля
    input_hash = get_password_hash(password)
    stored_hash = users_db[login]['hash']

    if input_hash == stored_hash:
        print(f"Вітаємо, {users_db[login]['full_name']}!")
    else:
        print("Помилка: Невірний пароль.")


def main_menu():

    while True:
        print("\n=== ГОЛОВНЕ МЕНЮ ===")
        print("1. Зареєструватися")
        print("2. Увійти")
        print("3. Вийти")

        choice = input("Ваш вибір (1-3): ")

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Роботу завершено.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main_menu()