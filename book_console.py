""" 
Данный модуль содержит функцию book_console, которая запускает консольное интерфейс для 
взаимодействия с библиотекой книг.

Эта функция представляет собой главный цикл программы, который отображает 
меню для пользователя, позволяя ему добавлять, удалять, искать книги, менять статус книг и 
получать данные по всем книгам которые есть в библиотеке. 
Она включает обработку пользовательского ввода, а также обработку 
ошибок, связанных с введенными данными, таких как отсутствие ввода, неверный 
формат или недопустимые значения.

В рамках этой функции выполняются следующие операции:
1. Отображение основного меню и ожидание выбора пользователя.
2. Добавление новой книги с запросом названия, автора и года издания.
3. Удаление книги по идентификатору, указанному пользователем.
4. Поиск книг по заданному критерию.
5. Вывод на экран всех книг, которые есть в библиотеки. 
6. Изменения статуса книги. 
7. Выход из программы.

При возникновении ошибок они логируются, и пользователю предоставляется 
обратная связь о причине сбоя. Все действия записываются в лог для 
последующего анализа.

Это функция является основным интерфейсом для работы с библиотекой и 
обеспечивает пользователю доступ ко всем основным операциям управления 
книгами.
"""

import logging
import time
from datetime import datetime
from book_class import Library
from menu import print_main_menu
from lexicon import LEXICON, LEXICON_LOG, LEXICON_STEP
from user_exception import (NotInputError, InvalidBookIDError, NotBookError, DisplayBookError, 
                            InvalidStatusError, DuplicateStatusError, YearBookError, InvalidBookIntError)


# Настройка логирования. Логи сохраняются в файл "book.log".
logging.basicConfig(
    filename = 'book.log',  
    level = logging.INFO,  
    format = '%(asctime)s - %(levelname)s - %(message)s', 
)


def book_console():
    logging.info(LEXICON_LOG['start'])
    # создается экземпляр класса библиотеки. Можно указать названия файла, по умолчанию - library.json
    library = Library() 
    
    # запуск цикла основного меню
    while True:
        logging.info(LEXICON_LOG['main_menu'])
        # загрузка полей меню
        print_main_menu()
        
        try:
            choice = (input(LEXICON['choice_menu']))
            # Проверяем наличие введенных данных на пустоту. Если поступила пустая строка - поднимает ошибку
            if not choice: 
                raise NotInputError
            # Проверяем, чтобы пользователь ввел число, а не строку
            if not choice.isdigit():
                raise ValueError(f'Меню может быть только из челых чисел')
            choice = int(choice)

            match choice:
                
                case 1: # Добавление книги в библиотеку
                    logging.info(LEXICON_LOG['add_book'])
                    # Запрашиваем у пользователя название, автора и год книги
                    title = input(LEXICON['add_book_title'])
                    author = input(LEXICON['add_book_author'])
                    year = input(LEXICON['add_book_year'])
                    try:
                        # Проверяем наличие введенных данных на пустоту. Если поступила пустая строка - поднимает ошибку
                        if not title or not author or not year:
                            raise NotInputError
                        # Проверяем правильность года. Если год меньше(равен) 0 или больше текущего кода - поднимает ошибку
                        if int(year) <= 0 or int(year) > datetime.now().year:
                            raise YearBookError(datetime.now().year)
                        # Проверяем чтобы год был числом, а не строкой. При не правильных данных - поднимает ошибку
                        if not year.isdigit():
                            raise InvalidBookIntError(year)
                        print(library.add_book(title, author, year))
                        logging.info(LEXICON_LOG['add_book_true'])
                    
                    except (NotInputError, YearBookError, InvalidBookIntError) as e:
                        # Выводим информацию в логи и пользователю в зависимости от ошибок
                        logging.error(f"{LEXICON_LOG['error_add_book']} {e}")
                        print(f"{LEXICON_STEP['exclamation_mark']}")
                        print(e)
                            

                case 2:  # Удаление книги из библиотеки
                    logging.info(LEXICON_LOG['delete_books'])
                    
                    try:
                        # Запрашиваем у пользователя id книги для удаления
                        book_id = input(LEXICON['delete_books_id'])
                        # Проверяем чтобы id был числом, а не строкой. При не правильных данных - поднимает ошибку
                        if not book_id.isdigit():
                            raise InvalidBookIntError(book_id)
                        print(library.remove_book(book_id))
                        logging.info(LEXICON_LOG['delete_books_true'])
                    except (NotInputError, InvalidBookIDError, InvalidBookIntError) as e:
                        # Выводим информацию в логи и пользователю в зависимости от ошибок
                        logging.error(f"{LEXICON_LOG['error_delete_books']} {e}")
                        print(f"{LEXICON_STEP['exclamation_mark']}")
                        print(e)
                    

                case 3: # Поиск книги в библиотеки
                    logging.info(LEXICON_LOG['search_books'])
                    try:
                        # Запрашиваем у пользователя название, автора или год книги для поиска
                        search_date = input(LEXICON['search_books_date'])
                        found_books = library.search_books(search_date)
                        # Выводим книги, которые найдены
                        for book in found_books:
                            print(LEXICON_STEP['lower'])
                            print(book.book_dict())
                        logging.info(LEXICON_LOG['search_books_true'])
                    except (NotBookError, NotInputError) as e:
                        # Выводим информацию в логи и пользователю в зависимости от ошибок
                        logging.error(f"{LEXICON_LOG['error_search_books']} {e}")
                        print(f"{LEXICON_STEP['exclamation_mark']}")
                        print(e)


                case 4: # Отображение всех книг в библиотеки
                    logging.info(LEXICON_LOG['display_books'])
                    try:
                        library_shows = library.display_books()
                        print(f"{LEXICON_STEP['lower']}")
                        print(f"{LEXICON_STEP['space']}{LEXICON['display_books_true']}")
                        print(f"{LEXICON_STEP['lower']}")
                        # Выводим книги, которые есть в библиотеки
                        for book in library_shows:
                            print(book.book_dict())
                        logging.info(LEXICON_LOG['display_books_true'])
                    except DisplayBookError as e:
                        # Выводим информацию в логи и пользователю в зависимости от ошибок
                        logging.error(e)
                        print(f"{LEXICON_STEP['exclamation_mark']}")
                        print(e)

                
                case 5: # Изменение статуса книги
                    logging.info(LEXICON_LOG['update_status'])
                    try:
                        # Запрашиваем у пользователя id книги
                        book_id = input(LEXICON['update_status_id'])
                        # Проверяем чтобы id был числом, а не строкой. При не правильных данных - поднимает ошибку
                        if not book_id.isdigit():
                            raise InvalidBookIntError(book_id)
                        # Запрашиваем у пользователя статус книги
                        new_status = input(LEXICON['update_status_input'])
                        print(library.update_status(book_id, new_status))
                        logging.info(LEXICON_LOG['update_status_true'])
                    except (InvalidBookIDError, InvalidStatusError, DuplicateStatusError, 
                            NotInputError, InvalidBookIntError) as e:
                        # Выводим информацию в логи и пользователю в зависимости от ошибок
                        logging.error(f"{LEXICON_LOG['error_update_status']} {e}")
                        print(f"{LEXICON_STEP['exclamation_mark']}")
                        print(e)

                case 6: # Завершение работы приложения
                    logging.info(LEXICON_LOG['exit_menu'])
                    print(f"{LEXICON['exit']} \n")
                    time.sleep(3)
                    print(f"{LEXICON_STEP['space']}{LEXICON_STEP['space']}{LEXICON['exit_end'].upper()}")
                    break
                
                case _: # обработка ошибок, если пользователь выбрал цифры, которые отсутствуют в меню
                    raise ValueError("Неверный выбор (в меню нет такого варианта)")


        except (ValueError, NotInputError) as e:
            # Выводим информацию в логи и пользователю в зависимости от ошибок
            logging.error(f"{LEXICON_LOG['exit_error']} {e}")
            print(f"{LEXICON_STEP['exclamation_mark']}")
            print(e)


