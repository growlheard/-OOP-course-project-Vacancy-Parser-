import json
import os


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, data_file):
        self.data_file = data_file
        self.__connect()

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        # проверяем, что файл существует и имеет расширение .json
        if os.path.isfile(value) and os.path.splitext(value)[1] == '.json':
            self.__data_file = value
        else:
            raise ValueError('Файла не существует или  формат не поддерживается')

        # проверяем целостность данных в файле
        with open(self.__data_file, 'r') as f:
            try:
                json.load(f)
            except json.JSONDecodeError:
                raise ValueError('Файл поврежден')

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        if not os.path.isfile(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)
        else:
            with open(self.data_file, 'r') as f:
                try:
                    json.load(f)
                except json.JSONDecodeError:
                    raise ValueError('Файл содержит ошибки')

    def insert(self, data):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        self.__connect()
        with open(self.data_file, 'r') as f:
            file_data = json.load(f)
        file_data.append(data)
        with open(self.data_file, 'w') as f:
            json.dump(file_data, f)

    def select(self, query):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        self.__connect()
        with open(self.data_file, 'r') as f:
            file_data = json.load(f)
        filtered_data = []
        for item in file_data:
            match = True
            for key, value in query.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                filtered_data.append(item)
        return filtered_data

    def delete(self, query):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if not len(query):
            return
        with open(self.__data_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            f.close()
        with open(self.__data_file, 'w', encoding='utf-8') as f:
            existing_data = list(
                filter(lambda item: not all(item[key] == value for key, value in query.items()), existing_data))

            json.dump(existing_data, f, indent=2, ensure_ascii=False)
            f.close()


