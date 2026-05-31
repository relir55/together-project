import sqlite3
from config import DATABASE

class LogicPayDB:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # Пользователи
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0.0
        )
            ''')

            # Платежи
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
            ''')

    def add_user(self, user_id, username):
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
                (user_id, username)
            )

    def get_user_balance(self, user_id):
        cursor = self.conn.execute(
            "SELECT balance FROM users WHERE user_id = ?", (user_id,)
        )
        result = cursor.fetchone()
        return result[0] if result else 0.0

    def update_balance(self, user_id, amount):
        with self.conn:
            self.conn.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (amount, user_id)
            )

    def create_payment(self, user_id, amount):
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO payments (user_id, amount) VALUES (?, ?)",
                (user_id, amount)
            )
            return cursor.lastrowid
