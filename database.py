import sqlite3

# Функція для створення бази даних та таблиці
def init_db():
    # Підключаємось до файлу бази (якщо його немає, він створиться)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Створюємо таблицю для зберігання ID користувачів
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

# Функція для додавання нового підписника
def add_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # INSERT OR IGNORE захищає від дублікатів (якщо користувач вже є в базі)
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

# Функція для отримання всіх ID (для розсилки)
def get_all_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()
    conn.close()
    # Перетворюємо список кортежів [(123,), (456,)] на звичайний список [123, 456]
    return [user[0] for user in users]