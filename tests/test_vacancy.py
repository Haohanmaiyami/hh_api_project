from vacancy import Vacancy


# Правильное создание объекта Vacancy
def test_vacancy_creation():
    vacancy = Vacancy(
        "Python Developer",
        "https://hh.ru/vacancy/123",
        150000,
        "Опыт от 3 лет",
    )
    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123"
    assert vacancy.salary == 150000
    assert vacancy.requirement == "Опыт от 3 лет"


# ЗП по умолчанию (если нет зарплаты)
def test_vacancy_salary_validation_zero():
    vacancy = Vacancy(
        "Python Developer", "https://hh.ru/vacancy/123", None, "Описание"
    )
    assert vacancy.salary == 0


# Сравнение вакансий по зарплате
def test_vacancy_comparison():
    vacancy1 = Vacancy("Dev1", "url1", 100000, "Desc1")
    vacancy2 = Vacancy("Dev2", "url2", 150000, "Desc2")
    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1
