from src.hh_api import HeadHunterAPI
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


def user_interaction():
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    keyword = input("Введите поисковый запрос: ")
    vacancies_data = hh_api.get_vacancies(keyword)
    vacancies = Vacancy.cast_to_object_list(vacancies_data)

    for vacancy in vacancies:
        json_saver.add_vacancy(vacancy)

    search_word = input("Введите ключевое слово для фильтрации вакансий: ")
    found_vacancies = json_saver.get_vacancies(search_word)

    if not found_vacancies:
        print("Вакансии не найдены.")
        return

    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    sorted_vacancies = sorted(found_vacancies, reverse=True)

    for vacancy in sorted_vacancies[:top_n]:
        print(f"Название: {vacancy.title}")
        print(f"Ссылка: {vacancy.url}")
        print(f"Зарплата: {vacancy.salary}")
        print(f"Требования: {vacancy.requirement}\n")


if __name__ == "__main__":
    user_interaction()
