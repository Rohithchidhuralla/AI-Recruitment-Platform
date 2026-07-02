import sqlite3


class UserDatabase:

    def __init__(self):

        self.conn = sqlite3.connect(
            "database/users.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT,

                email TEXT UNIQUE,

                password TEXT,

                role TEXT
            )
        """)

        self.conn.commit()

    def register_user(
        self,
        name,
        email,
        password,
        role
    ):

        self.cursor.execute(
            """
            INSERT INTO users
            (name,email,password,role)
            VALUES(?,?,?,?)
            """,
            (
                name,
                email,
                password,
                role
            )
        )

        self.conn.commit()

    def login(
        self,
        email,
        password
    ):

        self.cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email=?
            """,
            (email,)
        )

        return self.cursor.fetchone()
