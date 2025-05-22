import json
import os
import sys

from json_saver import JSONSaver
from vacancy import Vacancy

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


def test_add_vacancy():
    saver = JSONSaver(filename="test_vacancies.json")
    vacancy = Vacancy(
        "Python Dev", "https://hh.ru/vacancy/123", 150000, "Требуется опыт"
    )

    saver.add_vacancy(vacancy)

    assert os.path.exists("test_vacancies.json")

    with open("test_vacancies.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    assert any(item["url"] == "https://hh.ru/vacancy/123" for item in data)


def test_get_vacancies():
    saver = JSONSaver(filename="test_vacancies.json")

    found_vacancies = saver.get_vacancies("Python")

    assert len(found_vacancies) > 0
    assert "Python" in found_vacancies[0].title


def test_delete_vacancy():
    saver = JSONSaver(filename="test_vacancies.json")
    vacancy = Vacancy(
        "Python Dev", "https://hh.ru/vacancy/123", 150000, "Требуется опыт"
    )

    saver.delete_vacancy(vacancy)

    with open("test_vacancies.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    urls = [item["url"] for item in data]
    assert "https://hh.ru/vacancy/123" not in urls


def teardown_module(module):
    """Удалить тестовый файл после завершения всех тестов."""
    if os.path.exists("test_vacancies.json"):
        os.remove("test_vacancies.json")
