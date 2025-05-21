from typing import Any


class Vacancy:
    __slots__ = ("title", "url", "salary", "requirement")

    def __init__(self, title: str, url: str, salary: Any, requirement: str):
        self.title = title
        self.url = url
        self.salary = self.__validate_salary(salary)
        self.requirement = requirement

    def __validate_salary(self, salary: Any) -> int:
        if isinstance(salary, int):
            return salary
        return 0

    def __lt__(self, other: "Vacancy") -> bool:
        return self.salary < other.salary

    def __le__(self, other: "Vacancy") -> bool:
        return self.salary <= other.salary

    def __gt__(self, other: "Vacancy") -> bool:
        return self.salary > other.salary

    def __ge__(self, other: "Vacancy") -> bool:
        return self.salary >= other.salary

    @classmethod
    def cast_to_object_list(cls, vacancies_data: list) -> list:
        vacancies = []
        for item in vacancies_data:
            title = item.get("name")
            url = item.get("alternate_url")
            salary_info = item.get("salary")
            salary = (
                salary_info.get("from")
                if salary_info and salary_info.get("from")
                else 0
            )
            requirement = item.get("snippet", {}).get("requirement", "")
            vacancies.append(cls(title, url, salary, requirement))
        return vacancies

    # Новый метод для корректного сохранения в JSON
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "requirement": self.requirement,
        }
