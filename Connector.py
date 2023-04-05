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

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        if os.path.isfile(value) and os.path.splitext(value)[1] == '.json':
            self.__data_file = value
        else:
            raise ValueError('Файла не существует или  формат не поддерживается')

        with open(self.__data_file, 'r', encoding='utf-8') as f:
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
            with open(self.data_file, 'w', encoding='utf-8') as f:
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
        data = json.dumps(data, indent=2, ensure_ascii=False)
        with open(self.__data_file, "w", encoding='utf-8') as f:
            f.write(data)

    def select(self):
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        with open(self.__data_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            f.close()
        return existing_data

    def delete(self, file_name, query=None):
        if query is None:
            os.remove(file_name)
        else:
            existing_data = self.insert(file_name)
            if isinstance(existing_data, str):
                existing_data = json.loads(existing_data)
            updated_data = list(
                filter(lambda item: not all(item[key] == value for key, value in query.items()), existing_data))
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=4)
