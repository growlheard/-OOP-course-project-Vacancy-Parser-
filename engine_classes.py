import json
from abc import abstractmethod, ABC
import requests
from Connector import Connector
from jobs_classes import Vacancy


class Engine(ABC):
    @abstractmethod
    def get_request(self, url: str, params: dict, headers: dict):
        """Абстрактный метод для выполнения запроса
        на получение вакансий на сайтах"""
        vacancy = requests.get(url=url, params=params, headers=headers)
        return vacancy.json()

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        connector = Connector()
        connector.data_file = file_name
        return connector

    @staticmethod
    def save_to_json(data: list, file_name: str) -> None:
        """Метод для сохранения списка вакансий в json файл"""
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


class HH(Engine):
    """Класс HH для сбора вакансий с сайта hh.ru"""

    def __init__(self, hh_vacancy: str):
        """Конструктор класса HH"""
        self.hh_vacancy = hh_vacancy
        self.url = "https://api.hh.ru/vacancies"
        self.params = {'text': self.hh_vacancy, 'per_page': 100, 'page': 0, 'area': 113}
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    def get_request(self, **kwargs):
        """Метод для выполнения запроса на получение вакансий на сайте hh.ru"""
        return super().get_request(self.url, self.params, self.headers)


class SJ(Engine):
    """Класс SJ для сбора вакансий с сайта superjob.com"""

    def __init__(self, text: str):
        """Конструктор класса SJ"""
        self.text = text
        self.params = {'keywords': self.text, 'page': 0, 'count': 100}
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.headers = {'X-Api-App-Id': 'v3.r.137445108.c3d74d1ed555f025111419a0ce731232b93f95a0.bbb0327d9cdde4429c598a4ef8c34caffe152036'}

    def get_request(self, **kwargs):
        """Метод для выполнения запроса на получение вакансий на сайте superjob.com"""
        return super().get_request(self.url, self.params, self.headers)

