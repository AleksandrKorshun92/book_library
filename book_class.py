import json
import os
import logging
import datetime
from lexicon import LEXICON_LOG, LEXICON, LEXICON_STEP

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
        self.status: str = LEXICON['book_in_stock']
    
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
        print(f"{LEXICON_STEP['stars']}")
        print(f"{LEXICON['add_book_true']} {book.title}")
        print(f"{LEXICON_STEP['stars']}")
        self.next_id += 1
        self.save_books()


    def remove_book(self, book_id):
        try:
            if book_id in self.books:
                removed_book = self.books.pop(book_id)
                print(f"{LEXICON_STEP['stars']}")
                print(f"{LEXICON['delete_books_true']} {removed_book.id} c названием - {removed_book.title}")
                print(f"{LEXICON_STEP['stars']}")
                self.save_books()
        except Exception as e:
            logging.error(f"{LEXICON_LOG['error_delete_books_id']} {e}")
            print(f"{LEXICON['error_delete_books_id_not']} {book_id}")



    def search_books(self, search_date):
        try:
            found_books = [
            book for book in self.books.values()
            if (search_date.lower() in book.title.lower() or
                search_date.lower() in book.author.lower() or
                search_date.lower() in str(book.year).lower())
            ]
            return found_books
        except Exception as e:
            logging.error(f"{LEXICON_LOG['error_search_books']} {e}")
            print(f"{LEXICON['error_search_books']}")


    def display_books(self):
        if not self.books:
            return 
        else:
            books_library = [book for book in self.books.values()]
            return books_library


    def update_status(self, book_id, new_status):
        if book_id in self.books:
            if new_status in [LEXICON['book_in_stock'], LEXICON['book_is_missing']]:
                if self.books[book_id].status != new_status:
                    print(f"{LEXICON['update_status_true']} {self.books[book_id].book_dict()}")
                    self.save_books()
                else:
                    print(f"{LEXICON['error_update_status_repeat']} {new_status}") 
            else:
                print(LEXICON['error_update_status_input'])
        else:
            print(f"{LEXICON['error_update_status_id']} {book_id}")