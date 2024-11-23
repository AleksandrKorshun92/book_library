import json
import os
import logging
from lexicon import LEXICON_LOG, LEXICON, LEXICON_STEP
from user_exception import *

# Настройка логирования. Логи сохраняются в файл "book.log".
logging.basicConfig(
    filename = 'book.log',  
    level = logging.INFO,  
    format = '%(asctime)s - %(levelname)s - %(message)s', 
)

class Book:
    def __init__(self, book_id:int, title:str, author:str, year:str):
        self.id: int = book_id
        self.title: str = title
        self.author: str = author
        self.year: str = year
        self.status: str = 'в наличии'
    
    def book_dict(self) -> dict[str, str]:
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    @staticmethod
    def from_book_in_dict(data: dict[str, str]) -> 'Book':
        book = Book(data['id'], data['title'], data['author'], data['year'])
        book.status = data['status']
        return book
    

class Library:
    def __init__(self, filename:str='library.json'):
        self.filename: str = filename
        self.books: dict = {}
        self.next_id:int = 1
        self.load_books()

    def load_books(self):
        try: 
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
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
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                data = [book.book_dict() for book in self.books.values()]
                json.dump(data, f, ensure_ascii=False, indent=4)
                logging.info(LEXICON_LOG['save_books'])
        except OSError as e:
            logging.error(f"{LEXICON_LOG['error_save_books']} {e}")
            print(LEXICON['error_save_books'])
        except Exception as e:
            logging.error(f"{LEXICON_LOG['error_save_books']} {e}")
            print(LEXICON['error_save_books'])

    
    def add_book(self, title, author, year):     
        book = Book(self.next_id, title, author, int(year))
        self.books[self.next_id] = book
        self.next_id += 1
        self.save_books()
        print(f"{LEXICON_STEP['stars']}")
        return f"{LEXICON['add_book_true']} {book.title}\n {LEXICON_STEP['stars']}"


    def remove_book(self, book_id):
        # Проверяем наличие введенных данных на пустоту
        if not book_id:
            raise NotInputError
        book_id= int(book_id)
        
        # Проверяем наличие книги по ID
        if book_id not in self.books:
            raise InvalidBookIDError(book_id)
             
        if book_id in self.books:
            removed_book = self.books.pop(book_id)
            self.save_books()
            print(f"{LEXICON_STEP['stars']}")
            return f"{LEXICON['delete_books_true']} {removed_book.id} c названием - {removed_book.title}"
       

    def search_books(self, search_date):
        # Преобразуем поисковый запрос к нижнему регистру
        search_term = search_date.lower()
        
        if not search_date:
            raise NotInputError
        
        found_books = [
            book for book in self.books.values()
            if (search_term in book.title.lower() or
                search_term in book.author.lower() or
                search_term in str(book.year))
            ]
        
        if not found_books:
            raise NotBookError
        
        # Если все условия выполнены, возвращаем список книг
        return found_books


    def display_books(self):
        if not self.books:
            raise DisplayBookError 
        else:
            books_library = [book for book in self.books.values()]
            return books_library
    
    
    def update_status(self, book_id:int, new_status:str) ->str:
        # Проверяем наличие заполненных полей
        if not book_id or not new_status:
            raise NotInputError
        book_id = int(book_id)
        # Проверяем наличие книги по ID
        if book_id not in self.books:
            raise InvalidBookIDError(book_id)
            
        # Проверка допустимости нового статуса
        if new_status not in ['в наличии', 'выдана']:
            raise InvalidStatusError(new_status)

        current_book:Book = self.books[book_id]
        # Если новый статус совпадает со старым, выбрасываем исключение
        if current_book.status == new_status:
            raise DuplicateStatusError(new_status)

        else:
            # Обновляем статус книги
            current_book.status = new_status
            self.save_books()
            return f"{LEXICON['update_status_true']} {current_book.book_dict()}"

