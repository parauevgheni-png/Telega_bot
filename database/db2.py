import sqlite3

def init_db():
    conn = sqlite3.connect("films.db")
    cur = conn.cursor()

#database

    cur.execute("""
        CREATE TABLE IF NOT EXISTS films (
            title TEXT,
            year INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            comment TEXT,
            films TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_films():
    conn = sqlite3.connect("films.db")
    cur = conn.cursor()
    cur.execute("SELECT title, year FROM films")
    data = cur.fetchall()
    conn.close()
    return data


def add_film(title, year):
    conn = sqlite3.connect("films.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO films VALUES (?, ?)", (title, year))
    conn.commit()
    conn.close()