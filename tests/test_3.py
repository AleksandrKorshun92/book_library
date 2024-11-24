"""
Модуль для тестирования функциональности консольного интерфейса управления библиотекой книг.

Этот модуль содержит тесты для классов Book и Library, а также для основйнойконсольной команды 
book_console.
Использование фреймворк pytest и модуль unittest.mock для создания и использования моков.

Тесты охватывают:
- Инициализацию экземпляров класса Book.
- Преобразование экземпляра Book в словарь и обратно.
- Загрузку книг из JSON-файла в объект Library.
- Добавление новой книги в библиотеку.
- Эмуляцию консольных команд и взаимодействие с библиотекой через book_console.

Эти тесты помогают гарантировать правильную работу всех компонентов системы управления библиотекой книг.
"""

import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from book.book_console import book_console
from book.book_class import Library, Book
from book.lexicon import LEXICON, LEXICON_STEP


@pytest.fixture
def mock_library_json_file():
    """Создает мок для файла JSON, имитирующего библиотеку с тестовыми данными."""
    mock_data = json.dumps([{
        'id': 1,
        'title': 'Тестовое Название',
        'author': 'Тестовый Автор',
        'year': '2020',
        'status': 'в наличии'
    }])
    mock_file = mock_open(read_data=mock_data)
    with patch('builtins.open', mock_file):
        yield mock_file


@pytest.fixture
def mock_library():
    """Создаем мок для класса Library."""
    library_mock = MagicMock()
    return library_mock


def test_book_initialization():
    """Тестирует создание объекта Book и его атрибуты."""
    book = Book(1, 'Тестовое Название', 'Тестовый Автор', '2020')
    assert book.id == 1
    assert book.title == 'Тестовое Название'
    assert book.author == 'Тестовый Автор'
    assert book.year == '2020'
    assert book.status == 'в наличии'


def test_book_to_dict():
    """Тестирует преобразование объекта Book в словарь."""
    book = Book(1, 'Тестовое Название', 'Тестовый Автор', '2020')
    expected_dict = {
        'id': 1,
        'title': 'Тестовое Название',
        'author': 'Тестовый Автор',
        'year': '2020',
        'status': 'в наличии'
    }
    assert book.book_dict() == expected_dict


def test_book_from_dict():
    """Тестирует создание объекта Book из словаря."""
    data = {
        'id': 1,
        'title': 'Тестовое Название',
        'author': 'Тестовый Автор',
        'year': '2020',
        'status': 'в наличии'
    }
    book = Book.from_book_in_dict(data)
    assert book.title == 'Тестовое Название'
    assert book.author == 'Тестовый Автор'
    assert book.year == '2020'
    assert book.status == 'в наличии'


def test_library_add_book():
    """Тестирует добавление книги в библиотеку."""
    library = Library(filename='test_library.json')
    result = library.add_book('Тестовое Название', 'Тестовый Автор', '2020')
    assert result ==f"{LEXICON['add_book_true']} Тестовое Название\n {LEXICON_STEP['stars']}"
    assert library.books[1].title == 'Тестовое Название'  


def test_library_load_books(mock_library_json_file):
    """Тестирует загрузку книг из файла библиотеки JSON."""
    library = Library(filename='test_library.json')
    assert len(library.books) == 1
    assert library.books[1].title == 'Тестовое Название'


@patch('builtins.input')
@patch('menu.print_main_menu') 
def test_book_console_add_book(mock_print_main_menu, mock_input, mock_library):
    """Тестирует консольный интерфейс добавления книги."""
    
    # Указываем, что будет возвращать input
    mock_input.side_effect = [
        '1',               # Выбираем "Добавить книгу"
        'Горе программист', # Вводим название книги
        'Иванов',          # Вводим имя автора
        '1990',            # Вводим год
        '6'                # Указываем выход из программы
    ]
    
    # Указываем, что будет возвращать метод add_book
    mock_library.add_book.return_value = f"{LEXICON['add_book_true']} Петр\n {LEXICON_STEP['stars']}"

    with patch('book_console.Library', return_value=mock_library):  
        book_console()  # Запускаем консольный интерфейс
    
    # Проверяем, что add_book был вызван с правильными аргументами
    mock_library.add_book.assert_called_once_with('Горе программист', 'Иванов', '1990')
    

       
@patch('builtins.input')
@patch('menu.print_main_menu')
def test_book_console_delete_book(mock_print_main_menu, mock_input, mock_library):
    """Тестирует консольный интерфейс удаления книги."""

    mock_input.side_effect = [
        '2',               # Выбираем "Удалить книгу"
        '1',               # Указываем ID книги
        '6'                # Указываем выход из программы
    ]
    
    # Указываем, что будет возвращать метод remove_book
    mock_library.remove_book.return_value = "Книга удалена"

    with patch('book_console.Library', return_value=mock_library):  
        book_console()  # Запускаем консольный интерфейс
    
    # Проверяем, что remove_book был вызван с правильными аргументами
    mock_library.remove_book.assert_called_once_with('1')
    

@patch('builtins.input')
@patch('menu.print_main_menu')
def test_book_console_search_book(mock_print_main_menu, mock_input, mock_library):
    """Тестирует консольный интерфейс поиск книги."""

    mock_input.side_effect = [
        '3',               # Выбираем "Найти книгу"
        'Петр',             # Указываем название
        '6'                # Указываем выход из программы
    ]

    # Создаем объект книги
    library = Library(filename='test_library.json')
    mock_library = MagicMock()
    mock_library.search_books.return_value = [library.books[1]]  

    with patch('book_console.Library', return_value=mock_library): 
        book_console()  # Запускаем консольный интерфейс
    
    # Проверяем, что метод search_books был вызван с правильными аргументами
    mock_library.search_books.assert_called_once_with('Петр')


@patch('builtins.print') 
@patch('builtins.input')  
@patch('menu.print_main_menu')  
def test_book_console_display_books(mock_print_main_menu, mock_input, mock_print, mock_library):
    """Тестирует консольный интерфейс отображения книг из библиотеки."""

    mock_input.side_effect = [
        '4',               # Выбираем "Показать все книги библиотеки"
        '6'                # Указываем выход из программы
    ]

    # Создаем объекта библиотеки
    mock_library = MagicMock()

    # Создаем объекты книг
    book1 = Book(1, 'Тест Книга 1', 'Тест Автор 1', 1990)
    book2 = Book(2, 'Тест Книга 2', 'Тест Автор 2', 2020)
    
    mock_library.display_books.return_value = [book1, book2]


    with patch('book_console.Library', return_value=mock_library):  
        book_console()  # Запускаем консольный интерфейс

    # Проверяем, что метод display_books был вызван
    mock_library.display_books.assert_called_once()

    # Для проверки book_dict() на каждом выводе книги
    mock_print.assert_any_call(book1.book_dict())
    mock_print.assert_any_call(book2.book_dict())


@patch('builtins.input')
@patch('menu.print_main_menu')
def test_book_console_update_book(mock_print_main_menu, mock_input, mock_library):
    """Тестирует консольный интерфейс изменения статуса книги."""

    mock_input.side_effect = [
        '5',               # Выбираем "Найти книгу"
        '1',               # Выбираем id книги
        'выдана',          # Указываем статус книги
        '6'                # Указываем выход из программы
    ]

    # Создаем объект книги
    library = Library(filename='test_library.json')
    mock_library = MagicMock()
    mock_library.update_status.return_value = [library.books[1]]  

    with patch('book_console.Library', return_value=mock_library):  
        book_console()  # Запускаем консольный интерфейс
    
    # Проверяем, что метод update_status был вызван с правильными аргументами
    mock_library.update_status.assert_called_once_with('1', 'выдана')


if __name__ == "__main__":
    pytest.main()