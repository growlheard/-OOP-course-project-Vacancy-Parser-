import json
from datetime import datetime

CURRENCY_SYMBOLS = {
    'RUR': '₽',
    'RUB': '₽',
    'USD': '$',
    'EUR': '€',
}


def print_hh_vacancies(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        hh_vacancies = json.load(f)

    for vacancy_dict in hh_vacancies:
        vacancy = Vacancy(**vacancy_dict)
        formatted_vacancy = str(vacancy)
        print(formatted_vacancy)


class Vacancy:
    __slots__ = ['name', 'link', 'description', 'salary', 'city', 'date_published']

    def __init__(self, name, link, description, salary, city, date_published=None):
        self.name = name
        self.link = link
        self.description = description or ''
        self.salary = salary
        self.city = city
        if date_published is not None:
            if isinstance(date_published, str):
                self.date_published = date_published
            else:
                self.date_published = datetime.fromtimestamp(date_published).strftime('%Y-%m-%dT%H:%M:%S%z')
        else:
            self.date_published = None

    def get_salary(self):
        salary_min = 0
        if self.salary:
            salary_min = self.salary.get("min", 0)
            if salary_min:
                salary_min = int(salary_min.replace("\u202f", ""))
        return salary_min

    def get_salary_info(self):
        if self.salary:
            salary_from = self.salary.get('from')
            salary_to = self.salary.get('to')
            currency = self.salary.get('currency')
            if currency == 'RUR':
                currency = 'руб.'
            elif currency == 'USD':
                currency = 'USD'
            elif currency == 'EUR':
                currency = 'EUR'
            else:
                currency = ''
            if salary_from and salary_to:
                salary_info = f'{salary_from} - {salary_to} {currency}'
            elif salary_from:
                salary_info = f'от {salary_from} {currency}'
            elif salary_to:
                salary_info = f'до {salary_to} {currency}'
            else:
                salary_info = 'з/п не указана'
        else:
            salary_info = 'з/п не указана'
        return salary_info

    def to_dict(self):
        return {
            'name': self.name,
            'link': self.link,
            'description': self.description,
            'salary': self.salary,
            'city': self.city,
            'date_published': self.date_published
        }

    def __str__(self):
        name = self.name
        link = self.link
        description = self.description.replace('<highlighttext>', '').replace('</highlighttext>', '').strip()
        salary_info = self.get_salary_info()
        city = self.city
        date_published = self.date_published
        return f'ВРЕМЯ РАЗМЕЩЕНИЯ ВАКАНСИИ: {date_published}\n' \
               f'НАЗВАНИЕ ВАКАНСИИ: {name}\n' \
               f'ССЫЛКА НА ВАКАНСИЮ: {link}\nОПИСАНИЕ ВАКАНСИИ: {description}\nЗАРПЛАТА: {salary_info}\n' \
               f'ГОРОД: {city}\n '


class CountMixin:
    def __init__(self):
        self.data_file_json = None

    @property
    def get_count_of_vacancy(self):
        """
        Вернуть количество вакансий от текущего сервиса.
        Получать количество необходимо динамически из файла.
        """
        with open(self.data_file_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len(data)


class HHVacancy(Vacancy, CountMixin):  # add counter mixin
    """ HeadHunter Vacancy """
    hh_vacancies = []

    def __init__(self):
        super().__init__()
        self.salary_info = None
        self.city = None
        self.description = None
        self.link = None
        self.name = None
        self.data_file_json = 'hh_vacancy.json'

    def __str__(self):
        return f'НАЗВАНИЕ ВАКАНСИИ: {self.name}\n' \
               f'ССЫЛКА НА ВАКАНСИЮ: {self.link}\nОПИСАНИЕ ВАКАНСИИ: {self.description}\nЗАРПЛАТА: {self.salary_info}\n' \
               f'ГОРОД: {self.city}\n '


class SJVacancy(Vacancy, CountMixin):  # add counter mixin
    """ SuperJob Vacancy """
    sj_vacancies = []

    def __init__(self):
        super().__init__()
        self.salary_info = None
        self.city = None
        self.description = None
        self.link = None
        self.name = None
        self.data_file_json = 'sj_vacancy.json'

    def __str__(self):
        return f'НАЗВАНИЕ ВАКАНСИИ: {self.name}\n' \
               f'ССЫЛКА НА ВАКАНСИЮ: {self.link}\nОПИСАНИЕ ВАКАНСИИ: {self.description}\nЗАРПЛАТА: {self.salary_info}\n' \
               f'ГОРОД: {self.city}\n '


def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    return sorted(vacancies, key=lambda v: v.salary)


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    vacancies = sorting(vacancies)
    return iter(vacancies[:top_count])
