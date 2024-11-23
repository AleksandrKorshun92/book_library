""" 
- описание 
- теесты

"""

import logging
from datetime import datetime
import time
from book_class import Library
from lexicon import LEXICON, LEXICON_LOG, LEXICON_STEP
from user_exception import *


# Настройка логирования. Логи сохраняются в файл "book.log".
logging.basicConfig(
    filename = 'book.log',  
    level = logging.INFO,  
    format = '%(asctime)s - %(levelname)s - %(message)s', 
)


def book_console():
    logging.info(LEXICON_LOG['start'])
    library = Library()

    while True:
        logging.info(LEXICON_LOG['main_menu'])
        print(f"\n {LEXICON['main_menu']}")
        print(f"\n{LEXICON['add_book']}")
        print(LEXICON['delete_books'])
        print(LEXICON['search_books'])
        print(LEXICON['display_books'])
        print(LEXICON['update_status'])
        print(f"{LEXICON['exit_menu']}\n" )
        try:
            choice = (input(LEXICON['choice_menu']))
            if not choice: 
                raise NotInputError
            if not choice.isdigit():
                raise ValueError(f'Меню может быть только из челых чисел')
            choice = int(choice)

            match choice:
                
                case 1:
                    logging.info(LEXICON_LOG['add_book'])
                    while True:
                        title = input(LEXICON['add_book_title'])
                        author = input(LEXICON['add_book_author'])
                        year = input(LEXICON['add_book_year'])
                        try:
                            if not title or not author or not year:
                                raise NotInputError
                            if int(year) <= 0 or int(year) > datetime.now().year:
                                raise YearBookError(datetime.now().year)
                            if not year.isdigit():
                                raise InvalidBookIntError(year)
                            print(library.add_book(title, author, year))
                            logging.info(LEXICON_LOG['add_book_true'])
                            break
                    
                        except (NotInputError, YearBookError, InvalidBookIntError) as e:
                            logging.error(f"{LEXICON_LOG['error_add_book']} {e}")
                            print(f"{LEXICON_STEP['exclamation_mark']}")
                            print(e)

                            retry = input(LEXICON['add_book_retry'])
                            if retry.lower() == 0:
                                break
                            

                case 2:
                    logging.info(LEXICON_LOG['delete_books'])
                    
                    try:
                        book_id = input(LEXICON['delete_books_id'])
                        if not book_id.isdigit():
                            raise InvalidBookIntError(book_id)
                        print(library.remove_book(book_id))
                        logging.info(LEXICON_LOG['delete_books_true'])
                    except (NotInputError, InvalidBookIDError, InvalidBookIntError) as e:
                        logging.error(f"{LEXICON_LOG['error_delete_books']} {e}")
                        print(f"{LEXICON_STEP['exclamation_mark']}")
                        print(e)
                    

                case 3:
                    logging.info(LEXICON_LOG['search_books'])
                    try:
                        search_date = input(LEXICON['search_books_date'])
                        found_books = library.search_books(search_date)
                        for book in found_books:
                            print(LEXICON_STEP['lower'])
                            print(book.book_dict())
                        logging.info(LEXICON_LOG['search_books_true'])
                    except (NotBookError, NotInputError) as e:
                        logging.error(f"{LEXICON_LOG['error_search_books']} {e}")
                        print(f"{LEXICON_STEP['exclamation_mark']}")
                        print(e)


                case 4:
                    logging.info(LEXICON_LOG['display_books'])
                    try:
                        library_shows = library.display_books()
                        print(f"{LEXICON_STEP['lower']}")
                        print(f"{LEXICON_STEP['space']}{LEXICON['display_books_true']}")
                        print(f"{LEXICON_STEP['lower']}")
                        for book in library_shows:
                            print(book.book_dict())
                        logging.info(LEXICON_LOG['display_books_true'])
                    except DisplayBookError as e:
                        logging.error(e)
                        print(f"{LEXICON_STEP['exclamation_mark']}")
                        print(e)

                
                case 5:
                    logging.info(LEXICON_LOG['update_status'])
                    try:
                        book_id = input(LEXICON['update_status_id'])
                        if not book_id.isdigit():
                            raise InvalidBookIntError(book_id)
                        new_status = input(LEXICON['update_status_input'])
                        print(library.update_status(book_id, new_status))
                        logging.info(LEXICON_LOG['update_status_true'])
                    except (InvalidBookIDError, InvalidStatusError, DuplicateStatusError, 
                            NotInputError, InvalidBookIntError) as e:
                        logging.error(f"{LEXICON_LOG['error_update_status']} {e}")
                        print(f"{LEXICON_STEP['exclamation_mark']}")
                        print(e)

                case 6:
                    logging.info(LEXICON_LOG['exit_menu'])
                    print(f"{LEXICON['exit']} \n")
                    time.sleep(3)
                    print(f"{LEXICON_STEP['space']}{LEXICON_STEP['space']}{LEXICON['exit_end'].upper()}")
                    break
                
                case _:
                    raise ValueError("Неверный выбор (в меню нет такого варианта)")


        except (ValueError, NotInputError) as e:
            logging.error(f"{LEXICON_LOG['exit_error']} {e}")
            print(f"{LEXICON_STEP['exclamation_mark']}")
            print(e)


