from datetime import datetime

from engine_classes import *
from jobs_classes import Vacancy

import json


def get_sj_vacancies(keyword, pages=100, limit=None, ):
    """
    Функция для получения списка вакансий с сайта SuperJob.
    :param keyword:
    :param pages:
    :param limit:
    :return:
    """
    sj_vacancies = []
    sj_engine = SJ(keyword)
    for page in range(pages):
        sj_engine.params['page'] = page
        response = sj_engine.get_request()
        for vacancy_info in response['objects']:
            name = vacancy_info['profession']
            link = vacancy_info['link']
            description = vacancy_info['candidat']
            salary = vacancy_info['payment_from'] or vacancy_info['payment_to']
            if salary:
                salary = {"from": salary, "to": None, "currency": "RUB"}
            else:
                salary = None
            city = vacancy_info['town']['title']
            date_published = vacancy_info['date_published']
            vacancy = Vacancy(name, link, description, salary, city, date_published)
            sj_vacancies.append(vacancy)
            if len(sj_vacancies) == limit:
                break
        if len(sj_vacancies) == limit:
            break
    with open('sj_vacancies.json', 'w', encoding='utf-8') as f:
        json.dump([vacancy.to_dict() for vacancy in sj_vacancies], f, ensure_ascii=False, indent=4)

    print(f"{len(sj_vacancies)} vacancies found.")


def get_hh_vacancies(keyword: str) -> None:
    """
    Функция для получения списка вакансий с сайта HeadHunter.
    :param keyword:
    :return:
    """
    hh_vacancies = []
    hh_engine = HH(keyword)
    hh_data = hh_engine.get_request()
    for item in hh_data['items'][:1000]:
        name = item['name']
        link = item['alternate_url']
        description = item['snippet']['requirement']
        salary = item['salary']
        city = item['area']['name']
        date_published = item['published_at']
        vacancy = Vacancy(name, link, description, salary, city, date_published)
        hh_vacancies.append(vacancy)
    with open('hh_vacancies.json', 'w', encoding='utf-8') as f:
        json.dump([vacancy.to_dict() for vacancy in hh_vacancies], f, ensure_ascii=False, indent=4)

    print(f"Найдено {len(hh_vacancies)} вакансий.")


def print_sorted_vacancies(vacancies_file):
    """
    Сортировка вакансий по зарплате
    :param vacancies_file:
    :return:
    """
    with open(vacancies_file, 'r', encoding='utf-8') as f:
        vacancies = json.load(f)

    sorted_vacancies = sorted(vacancies, key=lambda x: (x['salary']['currency'] in ['USD', 'EUR'], x['salary']['from'])
    if x['salary'] is not None and x['salary']['from'] is not None else (False, 0), reverse=True)

    for vacancy_dict in sorted_vacancies:
        vacancy = Vacancy(**vacancy_dict)
        formatted_vacancy = str(vacancy)
        print(formatted_vacancy)


def print_sorted_vacancies_by_timeSJ(vacancies_file):
    """
    Сортировка вакансий с сайта SuperJob по времени размещения вакансий
    :param vacancies_file:
    :return:
    """
    with open(vacancies_file, 'r', encoding='utf-8') as f:
        vacancies = json.load(f)

    sorted_vacancies = sorted(vacancies, key=lambda x: datetime.strptime(x['date_published'],'%Y-%m-%dT%H:%M:%S'),
                              reverse=True)

    for vacancy_dict in sorted_vacancies:
        vacancy = Vacancy(**vacancy_dict)
        formatted_vacancy = str(vacancy)
        print(formatted_vacancy)


def print_sorted_vacancies_by_timeHH(vacancies_file):
    """
    Сортировка вакансий с сайта HeadHunter по времени размещения вакансий
    :param vacancies_file:
    :return:
    """
    with open(vacancies_file, 'r', encoding='utf-8') as f:
        vacancies = json.load(f)

    sorted_vacancies = sorted(vacancies, key=lambda x: datetime.strptime(x['date_published'],'%Y-%m-%dT%H:%M:%S%z'),
                              reverse=True)

    for vacancy_dict in sorted_vacancies:
        vacancy = Vacancy(**vacancy_dict)
        formatted_vacancy = str(vacancy)
        print(formatted_vacancy)


