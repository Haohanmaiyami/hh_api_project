import os
import sys
from unittest.mock import patch

import pytest

from hh_api import HeadHunterAPI

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)


# Тест успешного получения вакансий с hh.ru
@patch("hh_api.requests.get")  # Подменяем метод requests.get на фейковый
def test_get_vacancies_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"name": "Python Developer"}]}

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("Python")

    assert isinstance(vacancies, list)
    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Python Developer"


# Тест обработки ошибки подключения к API (статус код != 200)
@patch("hh_api.requests.get")
def test_get_vacancies_connection_error(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 500

    hh_api = HeadHunterAPI()

    with pytest.raises(ConnectionError):
        hh_api.get_vacancies("Python")
