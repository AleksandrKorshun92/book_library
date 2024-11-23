""" 
сделать лоигрование 
- ошибки - ошибка книги нет при поиске * ошибка при загрузки * 

- поиск - проверить, чтобы было сравнение с маленькой буквы
- теесты

"""

import logging
from datetime import datetime
from book_class import Library
from lexicon import LEXICON, LEXICON_LOG, LEXICON_STEP


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

        choice = int(input(LEXICON['choice_menu']))
        match choice:
            case 1:
                logging.info(LEXICON_LOG['add_book'])
                while True:
                    title = input(LEXICON['add_book_title'])
                    author = input(LEXICON['add_book_author'])
                    year = input(LEXICON['add_book_year'])
                    try:
                        if not title or not author or not year.isdigit():
                            logging.error(LEXICON_LOG['error_add_book'])
                            raise ValueError(LEXICON['error_add_book'])
                        if int(year) <= 0 or int(year) > datetime.now().year:
                            logging.error(LEXICON_LOG['error_add_book_year'])
                            raise ValueError(LEXICON['error_add_book_year'])
                        library.add_book(title, author, year)
                        logging.info(LEXICON_LOG['add_book_true'])
                        break
                    except ValueError as e:
                        print(LEXICON_STEP['equals'])
                        print(f'{e}')
                        print(f"{LEXICON_STEP['equals']} \n")
                        retry = input(LEXICON['add_book_retry'])
                        if retry.lower() == 'нет':
                            break
                        

            case 2:
                logging.info(LEXICON_LOG['delete_books'])
                try:
                    book_id = int(input(LEXICON['delete_books_id']))
                    if book_id <= 0:
                        logging.error(LEXICON_LOG['error_delete_books_id'])
                        raise ValueError(LEXICON['error_delete_books_id'])
                    library.remove_book(book_id)
                    logging.info(LEXICON_LOG['delete_books_true'])

                except ValueError as e:
                    logging.error(f"{LEXICON_LOG['error_delete_books_id']} {e}")
                    print(LEXICON_STEP['equals'])
                    print(LEXICON['error_delete_books_id'])
                    print(f"{LEXICON_STEP['equals']} \n")


            case 3:
                logging.info(LEXICON_LOG['search_books'])
                search_date = input(LEXICON['search_books_date'])
                found_books = library.search_books(search_date)
                if not found_books:
                    print(f"{LEXICON['error_search_books_null']} \n")
                    logging.error({LEXICON_LOG['error_search_books']})
                else:
                    for book in found_books:
                        print(LEXICON_STEP['lower'])
                        print(book.book_dict())
                    logging.info(LEXICON_LOG['delete_search_books_true'])



            case 4:
                logging.info(LEXICON_LOG['display_books'])
                library_shows = library.display_books()
                if not library_shows:
                    print(f"{LEXICON['error_display_books_null']} \n")
                    logging.error({LEXICON_LOG['error_display_books_null']})
                else:
                    print(f"{LEXICON_STEP['lower']}")
                    print(f"{LEXICON_STEP['space']}{LEXICON['display_books_true']}")
                    print(f"{LEXICON_STEP['lower']}")
                    for book in library_shows:
                        print(book.book_dict())
                    logging.info(LEXICON_LOG['display_books_true'])



            case 5:
                logging.info(LEXICON_LOG['update_status'])
                try:
                    book_id = int(input(LEXICON['update_status_id']))
                    new_status = input(LEXICON['update_status_input'])
                    library.update_status(book_id, new_status)
                    logging.info(LEXICON_LOG['update_status_true'])
                except ValueError as e:
                    logging.error(f"{LEXICON_LOG['error_update_status']} {e}")
                    print(LEXICON_STEP['equals'])
                    print(LEXICON['error_update_status'])
                    print(f"{LEXICON_STEP['equals']} \n")


            case 6:
                print("Выход из программы.")
                break

        # else:
        #     print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    book_console()