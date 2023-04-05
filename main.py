from utils import *


def Main():
    # Запрос у пользователя, какой сайт использовать
    site = input("Какой сайт использовать? (HeadHunter или SuperJob): ")
    # Запрос у пользователя названия вакансии
    keyword = input("Введите название вакансии: ")
    # Запрос у пользователя, по какому критерию сортировать результаты поиска
    sort_by = input("Сортировать по времени или зарплате? (время/зарплата): ")

    # Если выбран сайт HeadHunter
    if site.lower() == "headhunter" or site.lower() == "hh":
        # Получение списка вакансий HeadHunter, относящихся к данной вакансии
        get_hh_vacancies(keyword)

        # Создание экземпляра класса Connector для файла hh_vacancies.json
        hh_connector = Connector('hh_vacancies.json')

        # Если выбрана сортировка по времени
        if sort_by.lower() == "время" or sort_by.lower() == "time":
            # Печать отсортированного списка вакансий HeadHunter по времени
            print_sorted_vacancies_by_timeHH(hh_connector.data_file)
        # Если выбрана сортировка по зарплате
        elif sort_by.lower() == "зарплата" or sort_by.lower() == "salary":
            # Печать отсортированного списка вакансий HeadHunter по зарплате
            print_sorted_vacancies(hh_connector.data_file)
        # Если введен некорректный ввод критерия сортировки
        else:
            print("Неправильный ввод. Пожалуйста, введите 'время' или 'зарплата'.")

        # Удаление файла hh_vacancies.json
        hh_connector.delete('hh_vacancies.json')

    # Если выбран сайт SuperJob
    elif site.lower() == "superjob" or site.lower() == "sj":
        # Установка количества страниц и лимита вакансий
        pages = 100
        limit = 600
        # Получение списка вакансий SuperJob, относящихся к данной вакансии
        get_sj_vacancies(keyword, pages, limit)

        # Создание экземпляра класса Connector для файла sj_vacancies.json
        sj_connector = Connector('sj_vacancies.json')
        # Если выбрана сортировка по времени
        if sort_by.lower() == "время" or sort_by.lower() == "time":
            # Печать отсортированного списка вакансий SuperJob по времени
            print_sorted_vacancies_by_timeSJ(sj_connector.data_file)
        # Если выбрана сортировка по зарплате
        elif sort_by.lower() == "зарплата" or sort_by.lower() == "salary":
            # Печать отсортированного списка вакансий SuperJob по зарплате
            print_sorted_vacancies('sj_vacancies.json')
        # Если введен некорректный ввод критерия сортировки
        else:
            print("Неправильный ввод. Пожалуйста, введите 'время' или 'зарплата'.")
        # Если введен некорректный ввод сайта
            # Удаление файла sj_vacancies.json
        sj_connector.delete('sj_vacancies.json')
    else:
        print("Неправильный ввод. Пожалуйста, введите 'HeadHunter' или 'SuperJob'.")


if __name__ == '__main__':
    Main()
