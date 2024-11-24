import pytest
from unittest.mock import patch
from io import StringIO

from book_console import book_console
from book_class import Library, Book
from user_exception import *
from lexicon import *

@pytest.fixture
def mock_input(monkeypatch):
    """Фикстура для перехвата пользовательского ввода."""
    def mock_input_succeed(prompt):
        return prompt

    monkeypatch.setattr('builtins.input', mock_input_succeed)
    return mock_input_succeed


@pytest.fixture
def mock_print(monkeypatch):
    """Фикстура для перехвата вывода в консоль."""
    buffer = StringIO()
    monkeypatch.setattr('sys.stdout', buffer)
    return buffer


def test_book_console_add_book_success(mock_input, mock_print):
    # Тест успешного добавления книги
    with patch.object(Library, 'add_book') as mock_add_book:
        mock_add_book.return_value = "Книга успешно добавлена!"
        book_console()
    
    assert "Книга успешно добавлена!" in mock_print.getvalue()
    assert f"{LEXICON_LOG['add_book_true']}" in mock_print.getvalue()


def test_book_console_add_book_failure(mock_input, mock_print):
    # Тест неудачного добавления книги (например, при вводе неверного года издания)
    with patch.object(Library, 'add_book') as mock_add_book:
        mock_add_book.side_effect = Exception("Ошибка добавления книги!")
        book_console()
    
    assert "Ошибка добавления книги!" in mock_print.getvalue()
    assert f"{LEXICON_LOG['error_add_book']}" in mock_print.getvalue()


def test_book_console_delete_book_success(mock_input, mock_print):
    # Тест успешного удаления книги
    with patch.object(Library, 'remove_book') as mock_remove_book:
        mock_remove_book.return_value = "Книга успешно удалена!"
        book_console()
    
    assert "Книга успешно удалена!" in mock_print.getvalue()
    assert f"{LEXICON_LOG['delete_books_true']}" in mock_print.getvalue()


def test_book_console_delete_book_failure(mock_input, mock_print):
    # Тест неудачного удаления книги (например, при вводе несуществующего ID)
    with patch.object(Library, 'remove_book') as mock_remove_book:
        mock_remove_book.side_effect = Exception("Ошибка удаления книги!")
        book_console()
    
    assert "Ошибка удаления книги!" in mock_print.getvalue()
    assert f"{LEXICON_LOG['error_delete_books']}" in mock_print.getvalue()


def test_book_console_search_book_success(mock_input, mock_print):
    # Тест успешного поиска книг
    with patch.object(Library, 'search_books') as mock_search_books:
        mock_search_books.return_value = ["Книга 1", "Книга 2"]
        book_console()
    
    assert "Книга 1" in mock_print.getvalue()
    assert "Книга 2" in mock_print.getvalue()
    assert f"{LEXICON_LOG['search_books_true']}" in mock_print.getvalue()


def test_book_console_search_book_failure(mock_input, mock_print):
    # Тест неудачного поиска книг (например, при отсутствии книг в библиотеке)
    with patch.object(Library, 'search_books') as mock_search_books:
        mock_search_books.side_effect = Exception("Ошибка поиска книг!")
        book_console()
    
    assert "Ошибка поиска книг!" in mock_print.getvalue()
    assert f"{LEXICON_LOG['error_search_books']}" in mock_print.getvalue()
