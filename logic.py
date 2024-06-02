import sqlite3


class Person:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        con = sqlite3.connect('database.db')
        with con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS person (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    job TEXT NOT NULL,
                    interests TEXT NOT NULL,
                    feelings TEXT NOT NULL,
                    general TEXT NOT NULL
                )
            """)
            con.commit()

    def info(self, user_id, job, interests, feelings, general):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute(
                "INSERT INTO person (user_id, job, interests, feelings, general) VALUES (?, ?, ?, ?, ?)",
                (user_id, job, interests, feelings, general)
            )
            conn.commit()
