from abc import ABC, abstractmethod
from typing import Dict, List

import requests


# Абстрактный класс для работы с любым API вакансий
class JobAPI(ABC):
    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict]:
        pass


# Конкретная реализация для hh.ru
class HeadHunterAPI(JobAPI):
    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, keyword: str) -> List[Dict]:
        params = {"text": keyword, "per_page": 50}
        response = requests.get(self.__base_url, params=params)
        if response.status_code != 200:
            raise ConnectionError(
                f"Ошибка подключения к API: {response.status_code}"
            )
        return response.json().get("items", [])


def get_employer_data(employer_id: int) -> dict:
    """
    Получает данные о работодателе с hh.ru по ID.
    """
    url = f"https://api.hh.ru/employers/{employer_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_company_vacancies(employer_id: int) -> list:
    """
    Получает список вакансий от работодателя с hh.ru по ID.
    """
    url = "https://api.hh.ru/vacancies"
    params = {"employer_id": employer_id, "per_page": 100}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("items", [])
