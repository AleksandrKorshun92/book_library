""" 
Модуль библиотеки для управления книгами в виртуальной библиотеки.

Этот модуль предоставляет классы Book и Library, которые позволяют управлять коллекцией книг. 
Класс Book представляет собой отдельную книгу с характеристиками: 
- идентификатор (id),
- название (title),
- автор (author), 
- год издания (year)
- статус (status).
 
Класс Library представляет собой коллекцию книг и предоставляет методы для добавления, удаления, 
поиска, изменения статуса и сохранения книг в файле JSON. 

Пример использования:
# Создаем экземпляр библиотеки
my_library = Library('my_library.json')

# Добавляем новую книгу
my_library.add_book("Война и мир", "Лев Толстой", "1869")

# Поиск всех книг, содержащих слово "война" в названии, авторе или году издания
found_books = my_library.search_books("война")
for book in found_books:
    print(book.book_dict())
    
# Удаления книги по идентификатору 
my_library.remove_book("1")

# Показ всех книг, которые есть в библиотеки
my_library.display_books("1")
for book in found_books:
    print(book.book_dict())
"""


import json
import os
import logging
from typing import Dict, Any, List
from lexicon import LEXICON_LOG, LEXICON, LEXICON_STEP
from user_exception import (NotInputError, InvalidBookIDError, NotBookError, DisplayBookError, 
                            InvalidStatusError, DuplicateStatusError)


# Настройка логирования. Логи сохраняются в файл "book.log".
logging.basicConfig(
    filename = 'book.log',  
    level = logging.INFO,  
    format = '%(asctime)s - %(levelname)s - %(message)s', 
)


class Book:
    def __init__(self, book_id: int, title: str, author: str, year: str)-> None:
        """
        Инициализация экземпляра класса Book.

        :param book_id: Уникальный идентификатор книги.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        """
        self.id: int = book_id
        self.title: str = title
        self.author: str = author
        self.year: str = year
        self.status: str = 'в наличии'
    
    def book_dict(self) -> Dict[str, str]:
        """
        Возвращает словарь, представляющий книгу.

        :return: Словарь с информацией о книге, включая id, title, author, year и status.
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @staticmethod
    def from_book_in_dict(data: Dict[str, str]) -> 'Book':
        """
        Создает экземпляр Book из словаря.

        :param data: Словарь с данными, содержащими информацию о книге.
        :return: Экземпляр Book.
        :raises KeyError: если в словаре отсутствуют необходимые ключи.
        """
        book = Book(data['id'], data['title'], data['author'], data['year'])
        book.status = data['status']
        return book
    

class Library:
    def __init__(self, filename: str = 'library.json') -> None:
        """
        Инициализация экземпляра класса Library.

        :param filename: Имя файла для хранения данных о книгах. По умолчанию 'library.json'.
        """
        self.filename: str = filename
        self.books: dict = {}
        self.next_id: int = 1
        self.load_books()

    def load_books(self) -> None:
        """
        Загружает книги из файла JSON.

        Метод пытается открыть указанный файл и загрузить данные о книгах в словарь books.
        Если файл не существует или возникает ошибка при десериализации данных,
        записывает сообщение об ошибке в лог и выводит сообщение пользователю.
        """
        try: 
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data:List[Dict[str, Any]] = json.load(f)
                    for book_data in data:
                        book = Book.from_book_in_dict(book_data)
                        self.books[book.id] = book
                        if book.id >= self.next_id:
                            self.next_id = book.id + 1
            logging.info(LEXICON_LOG['load_library'])
        except (IOError, json.JSONDecodeError) as e:
            logging.error(f"{LEXICON_LOG['error_load_library']} {e}")
            print(LEXICON['error_load_library'])

    def save_books(self):
        """
        Сохраняет книги в файл JSON.

        Метод открывает файл для записи и сериализует данные о книгах из словаря books в формате JSON.
        Если при сохранении возникает ошибка, она записывается в лог и выводится сообщение об ошибке.
        """
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                data:List[Dict[str, Any]] = [book.book_dict() for book in self.books.values()]
                json.dump(data, f, ensure_ascii=False, indent=4)
                logging.info(LEXICON_LOG['save_books'])
        except OSError as e:
            logging.error(f"{LEXICON_LOG['error_save_books']} {e}")
            print(LEXICON['error_save_books'])
        except Exception as e:
            logging.error(f"{LEXICON_LOG['error_save_books']} {e}")
            print(LEXICON['error_save_books'])

    
    def add_book(self, title: str, author: str, year: str) -> str:
        """
        Добавляет новую книгу в библиотеку.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :return: Сообщение об успешном добавлении книги.
        """     
        book = Book(self.next_id, title, author, int(year))
        self.books[self.next_id] = book
        self.next_id += 1
        self.save_books()
        print(f"{LEXICON_STEP['stars']}")
        return f"{LEXICON['add_book_true']} {book.title}\n {LEXICON_STEP['stars']}"


    def remove_book(self, book_id: str) -> str:
        """
        Удаляет книгу из библиотеки по идентификатору.

        :param book_id: Идентификатор книги, которую нужно удалить. Должен быть строкой, 
                        которая будет преобразована в целое число.
        :raises NotInputError: Если ввод пустой.
        :raises InvalidBookIDError: Если книга с данным ID не найдена.
        :return: Сообщение об успешном удалении книги.
        """
        # Проверяем наличие введенных данных на пустоту. Если поступила пустая строка - поднимает ошибку
        if not book_id:
            raise NotInputError
        book_id= int(book_id)  
        
        # Проверяем наличие книги по ID. Если нет такого id, поднимает ошибку 
        if book_id not in self.books:
            raise InvalidBookIDError(book_id)
        
        # Если все условия выполнены, возвращаем информацию по удаленной книги 
        if book_id in self.books:
            removed_book = self.books.pop(book_id)
            self.save_books()
            print(f"{LEXICON_STEP['stars']}")
            return f"{LEXICON['delete_books_true']} {removed_book.id} c названием - {removed_book.title}"
       

    def search_books(self, search_date:str) -> List[Book]:
        """
        Ищет книги по заданному поисковому запросу.

        :param search_date: Строка, содержащая поисковый запрос. 
                            Используется для поиска по названию, автору и году.
        :raises NotInputError: Если ввод пустой.
        :raises NotBookError: Если не найдено ни одной книги по заданному запросу.
        :return: Список найденных книг.
        """
        # Преобразуем поисковый запрос к нижнему регистру
        search_term = search_date.lower()
        
        # Проверяем наличие введенных данных на пустоту. Если поступила пустая строка - поднимает ошибку
        if not search_date:
            raise NotInputError
        
        found_books = [
            book for book in self.books.values()
            if (search_term in book.title.lower() or
                search_term in book.author.lower() or
                search_term in str(book.year))
            ]
        
        # Проверяем наличие книги. Если такой книги нет (не нашли) - поднимаем ошибку
        if not found_books:
            raise NotBookError
        
        # Если все условия выполнены, возвращаем список книг
        return found_books


    def display_books(self) -> List[Book]:
        """
        Отображает все книги в библиотеке.

        :raises DisplayBookError: Если в библиотеке нет книг.
        :return: Список всех книг в библиотеке.
        """
        # Проверяем библиотеку на наличие книг. Если пусто - поднимаем ошибку
        if not self.books:
            raise DisplayBookError 
        # Если все условия выполнены, возвращаем список книг
        else:
            books_library = [book for book in self.books.values()]
            return books_library
    
    
    def update_status(self, book_id: int, new_status: str) -> str:
        """
        Обновляет статус книги по заданному идентификатору.

        :param book_id: Идентификатор книги, статус которой нужно обновить.
        :param new_status: Новый статус книги. Должен быть одним из допустимых значений: 'в наличии', 'выдана'.
        :raises NotInputError: Если идентификатор книги или новый статус пустые.
        :raises InvalidBookIDError: Если книга с данным идентификатором не найдена в библиотеке.
        :raises InvalidStatusError: Если новый статус не является допустимым.
        :raises DuplicateStatusError: Если новый статус совпадает с текущим статусом книги.
        :return: Сообщение об успешном обновлении статуса книги, включая информацию о книге.
        """
        
        # Проверяем наличие введенных данных на пустоту. Если поступила пустая строка - поднимает ошибку
        if not book_id or not new_status:
            raise NotInputError
        book_id = int(book_id)
        
        # Проверяем наличие книги по ID. Если нет такого id, поднимает ошибку 
        if book_id not in self.books:
            raise InvalidBookIDError(book_id)
            
        # Проверка допустимости нового статуса (корректность введенных данных) - поднимает ошибку 
        if new_status not in ['в наличии', 'выдана']:
            raise InvalidStatusError(new_status)

        current_book:Book = self.books[book_id]
        
        # Если новый статус совпадает со старым, выбрасываем исключение
        if current_book.status == new_status:
            raise DuplicateStatusError(new_status)
        
        # Если все условия выполнены, обновляем статус книги
        else:
            current_book.status = new_status
            self.save_books()
            return f"{LEXICON['update_status_true']} {current_book.book_dict()}"

