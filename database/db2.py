import sqlite3

#import sql

conn_f = sqlite3.connect("food.db")
cursor_f = conn_f.cursor()

#add food


cursor_f.executescript(
    '''
    CREATE TABLE IF NOT EXISTS food (
        name TEXT,
        price INT
    );
''')
conn_f.commit()
conn_f.close()

#table food


def food_insert(name, price):
    conn_f = sqlite3.connect("food.db")
    cursor_f = conn_f.cursor()
    cursor_f.execute("INSERT INTO food(name, price) VALUES (?, ?)", (name, price))
    conn_f.commit()
    conn_f.close()


#food name

def food_del(namee):
    conn_f = sqlite3.connect("food.db")
    cursor_f = conn_f.cursor()
    cursor_f.execute("DELETE FROM food WHERE name = ?" , (namee,))
    conn_f.commit()
    conn_f.close()

#delete food


def food_change(prod_name, name, price):
    conn_f = sqlite3.connect("food.db")
    cursor_f = conn_f.cursor()
    cursor_f.execute("UPDATE food SET name = ?, price = ? WHERE name = ?", (name, price, prod_name))
    conn_f.commit()
    conn_f.close()    


#price