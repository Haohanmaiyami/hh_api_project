from typing import List, Tuple

from psycopg2.extensions import connection


class DBManager:
    def __init__(self, conn: connection):
        """
        Инициализация менеджера с подключением к базе данных.
        """
        self.conn = conn

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Возвращает список всех компаний и количество вакансий у каждой.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, COUNT(v.vacancy_id)
                FROM employers e
                LEFT JOIN vacancies v ON e.employer_id = v.employer_id
                GROUP BY e.name;
            """
            )
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, int, str]]:
        """
        Возвращает список всех вакансий с указанием:
        название компании, вакансия, зарплата от, до, ссылка.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.employer_id;
            """
            )
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Возвращает среднюю зарплату по всем вакансиям.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT AVG(salary_from) "
                "FROM vacancies "
                "WHERE salary_from IS NOT NULL;"
            )
            result = cur.fetchone()[0]
            return result if result else 0

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, int]]:
        """
        Возвращает список вакансий, у которых зарплата выше средней.
        """
        avg = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT name, salary_from
                FROM vacancies
                WHERE salary_from > %s;
            """,
                (avg,),
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[str]:
        """
        Возвращает список названий вакансий, в которых
        встречается переданное слово.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT name FROM vacancies
                WHERE name ILIKE %s;
            """,
                (f"%{keyword}%",),
            )
            return [row[0] for row in cur.fetchall()]
