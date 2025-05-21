import sys
import os
from time import sleep

# Добавляем путь до src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
sys.path.append(src_path)

from db import get_connection, create_tables
from hh_api import get_employer_data, get_company_vacancies
from db_manager import DBManager

# 10 выбранных работодателей
company_ids = [
    1740,    # Яндекс
    3529,    # Сбер
    39305,   # Газпром нефть
    87021,   # WILDBERRIES
    80,      # Альфа-Банк
    4181,    # ВТБ
    4716984, # X5 Digital
    2748,    # Ростелеком
    1455,    # HeadHunter
    15478    # VK
]

def insert_employer(conn, employer):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO employers (employer_id, name, url) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
            (employer['id'], employer['name'], employer['alternate_url'])
        )
    conn.commit()

def insert_vacancies(conn, employer_id, vacancies):
    with conn.cursor() as cur:
        for v in vacancies:
            salary_from = v['salary']['from'] if v.get('salary') and v['salary'].get('from') else None
            salary_to = v['salary']['to'] if v.get('salary') and v['salary'].get('to') else None
            cur.execute(
                "INSERT INTO vacancies (employer_id, name, salary_from, salary_to, url) VALUES (%s, %s, %s, %s, %s);",
                (employer_id, v['name'], salary_from, salary_to, v['alternate_url'])
            )
    conn.commit()

if __name__ == "__main__":
    conn = get_connection()
    create_tables(conn)

    print(" Загружаем данные работодателей и вакансий...")

    for company_id in company_ids:
        employer = get_employer_data(company_id)
        insert_employer(conn, employer)

        vacancies = get_company_vacancies(company_id)
        insert_vacancies(conn, company_id, vacancies)
        print(f" Загружено: {employer['name']} ({len(vacancies)} вакансий)")
        sleep(0.2)  # чтобы не нагружать API

    print("\n Анализ данных через DBManager:\n")
    manager = DBManager(conn)

    print("Компании и количество вакансий:")
    for row in manager.get_companies_and_vacancies_count():
        print(f"- {row[0]}: {row[1]} вакансий")

    print("\nСредняя зарплата по всем вакансиям:")
    print(f"{manager.get_avg_salary():,.2f} ₽")

    print("\nВакансии с зарплатой выше средней:")
    for name, salary in manager.get_vacancies_with_higher_salary():
        print(f"- {name}: от {salary} ₽")

    print("\nВакансии, содержащие 'Python':")
    for name in manager.get_vacancies_with_keyword('Python'):
        print(f"- {name}")

    conn.close()
