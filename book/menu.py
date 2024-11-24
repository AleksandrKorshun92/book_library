"""
Функция для отображения главного меню приложения.

Меню содержит следующие пункты:
1. Добавить книгу в библиотеку
2. Удалить книгу из библиотеки
3. Найти книгу в библиотеке
4. Отобразить все книги из библиотеки
5. Обновить статус книги
6. Выход из программы
"""

from book.lexicon import LEXICON

def print_main_menu():
    print(f"\n {LEXICON['main_menu']}")
    print(f"\n{LEXICON['add_book']}")
    print(LEXICON['delete_books'])
    print(LEXICON['search_books'])
    print(LEXICON['display_books'])
    print(LEXICON['update_status'])
    print(f"{LEXICON['exit_menu']}\n" )