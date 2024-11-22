LEXICON_STEP: dict[str, str] = { 
    "upper": "-"*100,
    "lower": "_"*100,
    "equals": "="*100,
    "stars": "*"*100,
    }

LEXICON: dict[str, str] = {
    "main_menu": '📚 Основное меню библиотеки 📚',
    "add_book": '1. Добавить книгу',
    "delete_books": '2. Удалить книгу',
    "search_books": '3. Искать книгу',
    "display_books": '4. Отображать все книги',
    "update_status": '5. Изменить статус книги',
    "exit_menu": '6. Выход',
    "choice_menu": "Выберите действие из меню: ", 
    "add_book_title": "Введите название книги: ", 
    "add_book_author": "Введите автора книги: ", 
    "add_book_year": "Введите год издания книги: ", 
    "add_book_retry": "Повторно добавить книгу напишите (да) или выйте в меню (нет) - ", 
    "delete_books_id": "Введите ID книги для удаления: ",
    "delete_books_true": "Книга удалена: ",
    
    
    'error_load_library': "Не удалось загрузить библиотеку.",
    "error_save_books":"Ошибка при записи файла",
    "error_add_book": "Неверные данные: название, автор и год должны быть заполнены.Попробуйте еще раз.",
    "error_add_book_year": "Неверные года книги. Попробуйте еще раз.",
    "error_delete_books_id": "Неверный id книги",
    "error_delete_books_id_not": "Книга не найдена с id - ",
    
    'add_book_true': "Добавлена в библиотеку книга - ",
    'book_in_stock': "в наличии",
    'book_is_missing': "выдана",
    
    }


LEXICON_LOG: dict[str, str] = {
    "start": 'Запуск программы',
    "main_menu": 'Открытие основного меню',
    "add_book": 'Открыто меню - добавить книгу',
    "load_library": 'Книги загружены из файла в библиотеку',
    "error_load_library":"Ошибка при открытии файла библиотеки: ",
    'save_books': "Книга успешна сохранена",
    "error_save_books":"Ошибка при записи файла: ",
    "add_book_true": 'Новая книга добавлена в библиотеку',
    "error_add_book": "Неверные данные: название, автор и год должны быть заполнены.",
    "error_add_book_year": "Неверные года книги",
    
    "delete_books": 'Открыто меню - Удалить книгу',
    "error_delete_books_id": "Неверный id книги",
    "delete_books_true": 'Книга удалена из библиотеке',
    
    
    "search_books": '3. Искать книгу',
    "display_books": '4. Отображать все книги',
    "update_status": '5. Изменить статус книги',
    "exit_menu": '6. Выход',
    "choice_menu": "Выберите действие из меню: ", 
    "add_book_title": "Введите название книги: ", 
    "add_book_author": "Введите автора книги: ", 
    "add_book_year": "Введите год издания книги: ", 
    }