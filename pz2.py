class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.is_active = True

    def verify_password(self, password):
        return self.password_hash == password

class Administrator(User):
    def __init__(self, username, password_hash):
        super().__init__(username, password_hash)
        self.permissions = []

class RegularUser(User):
    def __init__(self, username, password_hash):
        super().__init__(username, password_hash)
        self.last_login_date = None

class GuestUser(User):
    def __init__(self, username, password_hash=""):
        super().__init__(username, password_hash)
        self.access_rights = "limited"

class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.username] = user

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.verify_password(password):
            return user
        return None


# приклад
if __name__ == "__main__":
    system = AccessControl()

    admin = Administrator("admin", "admin_pass")
    user = RegularUser("stepan", "user_pass")
    guest = GuestUser("guest_1")

    system.add_user(admin)
    system.add_user(user)
    system.add_user(guest)

    print("--- Спроба входу адміністратора (правильний пароль) ---")
    logged_in = system.authenticate_user("admin", "admin_pass")
    if logged_in:
        print(f"Успішно: {logged_in.username} (Роль: {type(logged_in).__name__})")
    else:
        print("Помилка входу")

    print("\n--- Спроба входу користувача (невірний пароль) ---")
    logged_in = system.authenticate_user("stepan", "wrong_pass")
    if logged_in:
        print(f"Успішно: {logged_in.username}")
    else:
        print("Помилка: невірні дані")