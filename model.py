# model.py
import sqlite3
from settings import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            highest_score INTEGER NOT NULL
        )
    """)
    conn.commit()
    
    conn.close()

def save_score(name, score):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if player already exists
    cursor.execute("SELECT highest_score FROM scores WHERE name = ?", (name,))
    row = cursor.fetchone()

    if row:
        # Update only if new score is higher
        if score > row[0]:
            cursor.execute("UPDATE scores SET highest_score = ? WHERE name = ?", (score, name))
    else:
        cursor.execute("INSERT INTO scores (name, highest_score) VALUES (?, ?)", (name, score))

    conn.commit()
    conn.close()

def get_top_scores(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, highest_score FROM scores ORDER BY highest_score DESC LIMIT ?", (limit,))
    results = cursor.fetchall()
    conn.close()
    return results