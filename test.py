

from book_console import book_console
from book_class import Library, Book
from user_exception import *
from lexicon import *
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_library():
    """Создаем мок для класса Library."""
    library_mock = MagicMock()
    return library_mock

@patch('builtins.input')
@patch('book_console.print_main_menu')  # Замените на фактический путь к функции
def test_book_console_add_book(mock_print_main_menu, mock_input, mock_library):
    """Тест добавления книги."""
    
    # Указываем, что будет возвращать input
    mock_input.side_effect = [
        '1',               # Выбираем "Добавить книгу"
        'Book Title',     # Вводим название книги
        'Author Name',    # Вводим имя автора
        '2023'            # Вводим год
    ]
    
    # Указываем, что будет возвращать метод add_book
    mock_library.add_book.return_value = "Новая книга добавлена в библиотеку"

    # Заменяем класс Library на наш мок внутри book_console
    with patch('book_console.Library', return_value=mock_library):  # Замените на фактический путь
        book_console()

    # Проверяем, что add_book был вызван с правильными аргументами
    mock_library.add_book.assert_called_once_with('Book Title', 'Author Name', '2023')

    # Можно добавить проверку вывода, если это необходимо:
    captured = capsys.readouterr()  # Если capsys используется
    assert "Новая книга добавлена в библиотеку" in captured.out


@patch('builtins.input')
@patch('book_console.Library', return_value=mock_library)
@patch('book_console.print_main_menu')
def test_book_console_invalid_year(mock_print_main_menu, mock_library, mock_input):
    """Тест ввода некорректного года при добавлении книги."""

    mock_input.side_effect = [
        '1',                # Выбираем "Добавить книгу"
        'Book Title',      # Вводим название книги
        'Author Name',     # Вводим имя автора
        '-100',            # Вводим некорректный год
        '0'                # Выбираем 0 (список книг)
    ]

    with patch('logging.error') as mock_logging_error:  # Мокируем логирование
        book_console()

        # Проверяем, что logging.error был вызван с ошибкой
        mock_logging_error.assert_any_call("Ошибка добавления книги: Некорректный год")

@patch('builtins.input')
@patch('book_console.Library', return_value=mock_library)
@patch('book_console.print_main_menu')
def test_book_console_delete_book(mock_print_main_menu, mock_library, mock_input):
    """Тест удаления книги."""

    mock_input.side_effect = [
        '2',               # Выбираем "Удалить книгу"
        '1',               # Указываем ID книги
        '0'                # Возврат в меню
    ]

    mock_library.remove_book.return_value = "Книга удалена"

    with patch('logging.info') as mock_logging_info:  # Мокируем логирование
        book_console()

        # Проверяем, что remove_book был вызван с правильными аргуементами
        mock_library.remove_book.assert_called_once_with('1')
        # Проверяем, что логирование сработало
        mock_logging_info.assert_any_call('Книга удалена')

if __name__ == "__main__":
    pytest.main()

