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
        # Создание экземпляра класса Connector для файла hh_vacancies.json
        hh_connector = Connector('vacancy.json')
        # Получение списка вакансий HeadHunter, относящихся к данной вакансии
        get_hh_vacancies(keyword, connector=hh_connector)

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

        delete_json = input("Удалить файл JSON? (да/нет): ")

        if delete_json.lower() == "да" or delete_json.lower() == "yes":
            hh_connector.delete('vacancy.json')
        elif delete_json.lower() == "нет":
            print("Файл JSON сохранен.")
        else:
            print("Неправильный ввод. Пожалуйста, введите 'да' или 'нет'.")

    # Если выбран сайт SuperJob
    elif site.lower() == "superjob" or site.lower() == "sj":
        # Установка количества страниц и лимита вакансий
        pages = 100
        limit = 600
        sj_connector = Connector('vacancy.json')
        # Получение списка вакансий SuperJob, относящихся к данной вакансии
        get_sj_vacancies(keyword, pages, limit, connector=sj_connector)
        # Если выбрана сортировка по времени
        if sort_by.lower() == "время" or sort_by.lower() == "time":
            # Печать отсортированного списка вакансий SuperJob по времени
            print_sorted_vacancies_by_timeSJ(sj_connector.data_file)
        # Если выбрана сортировка по зарплате
        elif sort_by.lower() == "зарплата" or sort_by.lower() == "salary":
            # Печать отсортированного списка вакансий SuperJob по зарплате
            print_sorted_vacancies('vacancy.json')
        # Если введен некорректный ввод критерия сортировки
        else:
            print("Неправильный ввод. Пожалуйста, введите 'время' или 'зарплата'.")
        # Если введен некорректный ввод сайта
            # Удаление файла sj_vacancies.json
        delete_json = input("Удалить файл JSON? (да/нет): ")

        if delete_json.lower() == "да" or delete_json.lower() == "yes":
            sj_connector.delete('vacancy.json')
        elif delete_json.lower() == "нет":
            print("Файл JSON сохранен.")
        else:
            print("Неправильный ввод. Пожалуйста, введите 'да' или 'нет'.")
    else:
        print("Неправильный ввод. Пожалуйста, введите 'HeadHunter' или 'SuperJob'.")


if __name__ == '__main__':
    Main()
