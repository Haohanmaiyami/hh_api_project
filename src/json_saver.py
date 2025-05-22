import json
from abc import ABC, abstractmethod
from typing import List

from vacancy import Vacancy


# Абстрактный класс для сохранения данных
class VacancySaver(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Vacancy]:
        pass


# Класс для сохранения вакансий в JSON-файл
class JSONSaver(VacancySaver):
    def __init__(self, filename: str = "data/vacancies.json"):
        self.__filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.__load_vacancies()
        if not any(v.url == vacancy.url for v in vacancies):
            vacancies.append(vacancy)
        self.__save_vacancies(vacancies)

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.__load_vacancies()
        vacancies = [v for v in vacancies if v.url != vacancy.url]
        self.__save_vacancies(vacancies)

    def get_vacancies(self, keyword: str) -> List[Vacancy]:
        vacancies = self.__load_vacancies()
        return [
            v
            for v in vacancies
            if keyword.lower() in v.title.lower()
            or (v.requirement and keyword.lower() in v.requirement.lower())
        ]

    def __load_vacancies(self) -> List[Vacancy]:
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Vacancy(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def __save_vacancies(self, vacancies: List[Vacancy]) -> None:
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(
                [v.to_dict() for v in vacancies],
                f,
                ensure_ascii=False,
                indent=4,
            )
