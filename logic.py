import sqlite3


class Person:
    con = sqlite3.connect('database.db')
    with con:
        con.execute("""CREATE TABLE person (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            job TEXT NOT NULL,
            interests TEXT NOT NULL,
            feelings TEXT NOT NULL
        )""")
        con.commit()


person = Person()
