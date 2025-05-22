import os

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection

# Загрузка .env переменных
load_dotenv()


def get_connection() -> connection:
    """Подключение к базе данных PostgreSQL"""
    return connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )


def create_tables(conn: connection) -> None:
    """Создаёт таблицы employers и vacancies"""
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS vacancies;")
        cur.execute("DROP TABLE IF EXISTS employers;")

        cur.execute(
            """
        CREATE TABLE employers (
            employer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT
        );
        """
        )

        cur.execute(
            """
        CREATE TABLE vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(employer_id),
            name TEXT NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            url TEXT
        );
        """
        )

        conn.commit()
