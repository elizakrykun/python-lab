import hashlib


def generate_file_hashes(*file_paths):

    hashes_dict = {}

    for file_path in file_paths:
        try:
            sha256_hash = hashlib.sha256()

            with open(file_path, "rb") as f:

                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)

            file_hash = sha256_hash.hexdigest()

            hashes_dict[file_path] = file_hash

        except FileNotFoundError:
            print(f"Помилка: Файл '{file_path}' не знайдено.")
        except IOError:
            print(f"Помилка: Не вдалося прочитати файл '{file_path}'.")
        except Exception as e:
            print(f"Помилка при обробці '{file_path}': {e}")

    return hashes_dict


# приклад
if __name__ == "__main__":

    with open("test1.txt", "w") as f:
        f.write("Hello World")
    with open("test2.txt", "w") as f:
        f.write("Python is great")

    result = generate_file_hashes("test1.txt", "test2.txt", "missing_file.txt")


    print("\n--- Результат роботи ---")
    for path, hash_val in result.items():
        print(f"Файл: {path}\nХеш:  {hash_val}")