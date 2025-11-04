import sqlite3
from typing import Optional

DB_PATH = "users.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    # users table uses email as primary key
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        full_name TEXT DEFAULT "",
        age INTEGER,
        bio TEXT DEFAULT "",
        reset_token TEXT DEFAULT NULL
    )
    ''')
    # store each text + cleaned + sentiment + timestamp
    c.execute('''
    CREATE TABLE IF NOT EXISTS sentiment_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        original_text TEXT NOT NULL,
        cleaned_text TEXT,
        sentiment_label TEXT,
        sentiment_score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(email) REFERENCES users(email)
    )
    ''')
    conn.commit()
    conn.close()

# helper functions interacting with DB
def user_exists(email: str) -> bool:
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT 1 FROM users WHERE email = ?', (email,))
    r = c.fetchone()
    conn.close()
    return bool(r)

def add_user(email: str, hashed_password: str, full_name: str="", age: int=None, bio: str=""):
    conn = get_conn()
    c = conn.cursor()
    c.execute('INSERT INTO users(email, password, full_name, age, bio) VALUES (?, ?, ?, ?, ?)',
              (email, hashed_password, full_name, age, bio))
    conn.commit()
    conn.close()

def get_user_password(email: str) -> Optional[str]:
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE email = ?', (email,))
    row = c.fetchone()
    conn.close()
    return row['password'] if row else None

def set_reset_token(email: str, token: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute('UPDATE users SET reset_token = ? WHERE email = ?', (token, email))
    conn.commit()
    conn.close()

def get_reset_token(email: str) -> Optional[str]:
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT reset_token FROM users WHERE email = ?', (email,))
    row = c.fetchone()
    conn.close()
    return row['reset_token'] if row else None

def update_password(email: str, hashed_password: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute('UPDATE users SET password = ?, reset_token = NULL WHERE email = ?',
              (hashed_password, email))
    conn.commit()
    conn.close()

def save_sentiment_record(email: str, original_text: str, cleaned_text: str, sentiment_label: str, score: float):
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        INSERT INTO sentiment_records(email, original_text, cleaned_text, sentiment_label, sentiment_score)
        VALUES (?, ?, ?, ?, ?)
    ''', (email, original_text, cleaned_text, sentiment_label, score))
    conn.commit()
    conn.close()

def fetch_user_records(email: str):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM sentiment_records WHERE email = ? ORDER BY created_at DESC', (email,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_batch_records(email: str, records: list):
    # records: list of tuples (original, cleaned, label, score)
    conn = get_conn()
    c = conn.cursor()
    c.executemany('''
      INSERT INTO sentiment_records(email, original_text, cleaned_text, sentiment_label, sentiment_score)
      VALUES (?, ?, ?, ?, ?)
    ''', [(email, o, c_text, lbl, score) for (o, c_text, lbl, score) in records])
    conn.commit()
    conn.close()
