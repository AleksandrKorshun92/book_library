
import json
import os
from unittest.mock import patch, mock_open, MagicMock

from book_console import book_console
from book_class import Library, Book
from user_exception import *
from lexicon import *





# Test the Book class
def test_book_initialization():
    book = Book(1, 'Test Title', 'Test Author', '2023')
    assert book.id == 1
    assert book.title == 'Test Title'
    assert book.author == 'Test Author'
    assert book.year == '2023'
    assert book.status == 'в наличии'


def test_book_to_dict():
    book = Book(1, 'Test Title', 'Test Author', '2023')
    expected_dict = {
        'id': 1,
        'title': 'Test Title',
        'author': 'Test Author',
        'year': '2023',
        'status': 'в наличии'
    }
    assert book.book_dict() == expected_dict


def test_book_from_dict():
    data = {
        'id': 1,
        'title': 'Test Title',
        'author': 'Test Author',
        'year': '2023',
        'status': 'в наличии'
    }
    book = Book.from_book_in_dict(data)
    assert book.title == 'Test Title'
    assert book.author == 'Test Author'
    assert book.year == '2023'
    assert book.status == 'в наличии'


# Test the Library class
@pytest.fixture
def mock_library_json_file():
    mock_data = json.dumps([{
        'id': 1,
        'title': 'Test Title',
        'author': 'Test Author',
        'year': '2023',
        'status': 'в наличии'
    }])
    mock_file = mock_open(read_data=mock_data)
    with patch('builtins.open', mock_file):
        yield mock_file

def test_library_load_books(mock_library_json_file):
    library = Library(filename='test_library.json')
    assert len(library.books) == 1
    assert library.books[1].title == 'Test Title'


# @patch('builtins.open', new_callable=mock_open)
# def test_library_save_books(mock_open):
#     library = Library(filename='test_library.json')
#     library.add_book('New Book', 'New Author', '2024')
    
#     library.save_books()  # Вызываем, чтобы сохранить книгу
    
#     # Получаем все вызовы метода write
#     handle = mock_open()
#     handle().write.assert_called()  # Проверяем, был ли вызван метод write

#     # Извлекаем все вызовы метода write и собираем данные
#     written_calls = handle().write.call_args_list
#     written_data = ''.join(call[0][0] for call in written_calls)  # Объединяем все данные

#     saved_data = json.loads(written_data)  # Извлекаем данные
#     assert len(saved_data) == 1  # Убедимся, что только одна книга сохранена
#     assert saved_data[0]['title'] == 'New Book'
#     assert saved_data[0]['author'] == 'New Author'
#     assert saved_data[0]['year'] == '2024'    


def test_library_add_book():
    library = Library(filename='test_library.json')
    result = library.add_book('Test Book', 'Test Author', '2023')
    assert result ==f"{LEXICON['add_book_true']} Test Book\n {LEXICON_STEP['stars']}"
    assert library.books[1].title == 'Test Book'  # Check details of the added book


# @pytest.mark.parametrize("year", ["not_a_year", "-1", "2025"])  # Add any parameters you'd like to test
# def test_library_add_book_invalid_year_param(year: Literal['not_a_year'] | Literal['-1'] | Literal['2025']):
#     library = Library(filename='test_library.json')
#     if year == "not_a_year":
#         with pytest.raises(InvalidBookIntError):
#             library.add_book('Test Book', 'Test Author', year)  # Invalid input: year is not a number
#     else:
#         with pytest.raises(YearBookError):
#             library.add_book('Test Book', 'Test Author', year)





@pytest.fixture
def mock_library():
    """Создаем мок для класса Library."""
    library_mock = MagicMock()
    return library_mock

@patch('builtins.input')
@patch('menu.print_main_menu')  # Замените на фактический путь к функции
def test_book_console_add_book(mock_print_main_menu, mock_input, mock_library):
    """Тест добавления книги."""
    
    # Указываем, что будет возвращать input
    mock_input.side_effect = [
        '1',               # Выбираем "Добавить книгу"
        'Петр',           # Вводим название книги
        'Иванов',         # Вводим имя автора
        '12',             # Вводим год
        '6'               # Затем указываем выход из программы
    ]
    
    # Указываем, что будет возвращать метод add_book
    mock_library.add_book.return_value = f"{LEXICON['add_book_true']} Петр\n {LEXICON_STEP['stars']}"

    # Заменяем класс Library на наш мок внутри book_console
    with patch('book_console.Library', return_value=mock_library):  # Замените на фактический путь
        book_console()  # Запускаем консольный интерфейс
    
    # Проверяем, что add_book был вызван с правильными аргументами
    mock_library.add_book.assert_called_once_with('Петр', 'Иванов', '12')
    
    # Проверяем, что программа завершилась после выбора "6"
    # Здесь вы можете добавить дополнительные проверки, если это необходимо.

# @patch('builtins.input')
# @patch('book_console.Library', return_value=mock_library)
# @patch('menu.print_main_menu')
# def test_book_console_invalid_year(mock_print_main_menu, mock_library, mock_input):
#     """Тест ввода некорректного года при добавлении книги."""

#     mock_input.side_effect = [
#         '1',                # Выбираем "Добавить книгу"
#         'Book Title',      # Вводим название книги
#         'Author Name',     # Вводим имя автора
#         '2050',            # Вводим некорректный год
#         '6'
#     ]

#     # Создаем экземпляр mock_library
#     mock_library = MagicMock()

#     # Указываем, что метод add_book будет вызывать YearBookError
#     mock_library.add_book.side_effect = YearBookError

#     # Проверяем, что возникает ошибка при вызове book_console
#     with pytest.raises(YearBookError):
#         book_console()

#     # Проверяем, что add_book был вызван с правильными аргументами
#     mock_library.add_book.assert_called_once_with('Book Title', 'Author Name', '2050')


       
@patch('builtins.input')
@patch('menu.print_main_menu')
def test_book_console_delete_book(mock_print_main_menu, mock_input, mock_library):
    """Тест удаления книги."""

    mock_input.side_effect = [
        '2',               # Выбираем "Удалить книгу"
        '1',               # Указываем ID книги
        '6'                # Возврат в меню
    ]

    mock_library.remove_book.return_value = "Книга удалена"

    with patch('book_console.Library', return_value=mock_library):  # Замените на фактический путь
        book_console()  # Запускаем консольный интерфейс
    
    # Проверяем, что add_book был вызван с правильными аргументами
    mock_library.remove_book.assert_called_once_with('1')
    

@patch('builtins.input')
@patch('menu.print_main_menu')
def test_book_console_search_book(mock_print_main_menu, mock_input, mock_library):
    """Тест поиска книги."""

    mock_input.side_effect = [
        '3',               # Выбираем "Найти книгу"
        'Петр',              # Указываем название
        '6'                # Выход из программы
    ]

    # Создаем объект книги
    library = Library(filename='test_library.json')
    mock_library = MagicMock()
    mock_library.search_books.return_value = [library.books[1]]  # Теперь он возвращает список объектов книг

    with patch('book_console.Library', return_value=mock_library):  # Замените на фактический путь
        book_console()  # Запускаем консольный интерфейс
    
    # Проверяем, что метод search_books был вызван с правильными аргументами
    mock_library.search_books.assert_called_once_with('Петр')


@patch('builtins.print')  # Патчим print, чтобы перехватить вывод
@patch('builtins.input')  # Патчим print, чтобы перехватить вывод
@patch('menu.print_main_menu')  # Патчим print_main_menu
def test_book_console_display_books(mock_print_main_menu, mock_input, mock_print, mock_library):
    """Тест отображения книг."""

    mock_input.side_effect = [
        '4',               # Выбираем "Показать все книги библиотеки"
        '6'                # Выход из программы
    ]

    # Создаем мок объекта библиотеки
    mock_library = MagicMock()

    # Создаем объекты книг
    book1 = Book(1, 'Книга 1', 'Автор 1', 2020)
    book2 = Book(2, 'Книга 2', 'Автор 2', 2019)
    
    # Настраиваем мок библиотеки для возврата списка книг
    mock_library.display_books.return_value = [book1, book2]

    # Патчим класс Library, чтобы возвращался mock_library
    with patch('book_console.Library', return_value=mock_library):  # Замените на фактический путь
        book_console()  # Запускаем консольный интерфейс

    # Проверяем, что метод display_books был вызван
    mock_library.display_books.assert_called_once()

       # Для проверки book_dict() на каждом выводе книги
    mock_print.assert_any_call(book1.book_dict())
    mock_print.assert_any_call(book2.book_dict())


@patch('builtins.input')
@patch('menu.print_main_menu')
def test_book_console_update_book(mock_print_main_menu, mock_input, mock_library):
    """Тест поиска книги."""

    mock_input.side_effect = [
        '5',               # Выбираем "Найти книгу"
        '1',              #id
        'выдана',              #статус книги
        '6'                # Выход из программы
    ]

    # Создаем объект книги
    library = Library(filename='test_library.json')
    mock_library = MagicMock()
    mock_library.update_status.return_value = [library.books[1]]  # Теперь он возвращает список объектов книг

    with patch('book_console.Library', return_value=mock_library):  # Замените на фактический путь
        book_console()  # Запускаем консольный интерфейс
    
    # Проверяем, что метод search_books был вызван с правильными аргументами
    mock_library.update_status.assert_called_once_with('1', 'выдана')



if __name__ == "__main__":
    pytest.main()