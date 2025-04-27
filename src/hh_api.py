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
