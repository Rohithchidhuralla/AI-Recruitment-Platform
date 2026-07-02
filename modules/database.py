import os
import json
import sqlite3

BASE_DIR = "data"
USERS_FILE = os.path.join(BASE_DIR, "users.json")
RESUMES_FILE = os.path.join(BASE_DIR, "resumes.json")
DATABASE_DIR = "database"
RECRUITMENT_DB = os.path.join(DATABASE_DIR, "recruitment.db")


def ensure_storage():
    """Create data folder and JSON files if not exist"""
    os.makedirs(BASE_DIR, exist_ok=True)

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f)

    if not os.path.exists(RESUMES_FILE):
        with open(RESUMES_FILE, "w") as f:
            json.dump([], f)


def load_data(file_path):
    ensure_storage()
    with open(file_path, "r") as f:
        return json.load(f)


def save_data(file_path, data):
    ensure_storage()
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def get_users():
    return load_data(USERS_FILE)


def save_users(users):
    save_data(USERS_FILE, users)


def get_resumes():
    return load_data(RESUMES_FILE)


def save_resumes(resumes):
    save_data(RESUMES_FILE, resumes)


class Database:

    def __init__(self):

        os.makedirs(DATABASE_DIR, exist_ok=True)

        self.conn = sqlite3.connect(
            RECRUITMENT_DB,
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS candidates(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                ats_score INTEGER,
                skills TEXT,
                file_name TEXT
            )
            """
        )

        self.cursor.execute("PRAGMA table_info(candidates)")
        columns = [column[1] for column in self.cursor.fetchall()]

        if "file_name" not in columns:
            self.cursor.execute(
                "ALTER TABLE candidates ADD COLUMN file_name TEXT"
            )

        if "resume" in columns:
            self.cursor.execute(
                """
                UPDATE candidates
                SET file_name = resume
                WHERE file_name IS NULL
                """
            )

        self.conn.commit()

    def insert_candidate(
        self,
        name,
        email,
        phone,
        ats_score,
        skills,
        file_name
    ):

        if isinstance(skills, list):
            skills = ", ".join(skills)

        self.cursor.execute(
            """
            INSERT INTO candidates
            (name,email,phone,ats_score,skills,file_name)
            VALUES(?,?,?,?,?,?)
            """,
            (
                name,
                email,
                phone,
                ats_score,
                skills,
                file_name
            )
        )

        self.conn.commit()

    def get_candidates(self):

        self.cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                phone,
                ats_score,
                skills,
                file_name
            FROM candidates
            ORDER BY ats_score DESC, id DESC
            """
        )

        return self.cursor.fetchall()
