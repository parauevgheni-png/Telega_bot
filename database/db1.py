import sqlite3

#import sql

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

#import food

cursor.execute('''
    CREATE TABLE IF NOT EXISTS order(
              id INTEGER PRIMARY KEY,
              food_type TEXT,
              name_client TEXT,
              adress TEXT,
              phone_number TEXT
              )
''')

#import order

conn.commit()
conn.close()

#end of order