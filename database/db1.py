import sqlite3

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS order(
              id INTEGER PRIMARY KEY,
              food_type TEXT,
              name_client TEXT,
              adress TEXT,
              phone_number TEXT
              )
''')
conn.commit()
conn.close()