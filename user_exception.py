class BookError(Exception):
    """Базовый класс для всех ошибок, связанных с книгами."""
    pass


class InvalidBookIntError(BookError):
    """Ошибка, возникающая при передаче строки, а не числового значения"""
    def __init__(self, num):
        super().__init__()
        self.num = num

    def __str__(self):
        return f"Должна быть цифра, а не строка - {self.bonumok_id}"


class YearBookError(BookError):
    """Ошибка, возникающая при не правильном указание года (меньше 0 или больше текущего года)"""

    def __init__(self, year):
        super().__init__()
        self.year = year

    def __str__(self):
        return f"Год книги не может быть меньше '0' и больше текущего года {self.year}"

class NotInputError(BookError):
    """Ошибка, возникающая при отсутствии введенных данных (пустые поля)"""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Ошибка ввода данных (пустые поля)"

class NotBookError(BookError):
    """Ошибка, возникающая при отсутствии книги по переданным данным"""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Такая книга не найдена"


class DisplayBookError(BookError):
    """Ошибка, возникающая при загрузки книг из библиотеки."""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Библиотека пустая (надо скачать больше книг)"

class InvalidBookIDError(BookError):
    """Ошибка, возникающая при передаче неверного ID книги."""
    def __init__(self, book_id):
        super().__init__()
        self.book_id = book_id

    def __str__(self):
        return f"Книга не найдена c id - {self.book_id}"


class InvalidStatusError(BookError):
    """Ошибка, возникающая при попытке установить недопустимый статус."""
    def __init__(self, status):
        super().__init__()
        self.status = status

    def __str__(self):
        return f"Ошибка обновления статуса: {self.status}"

class DuplicateStatusError(BookError):
    """Ошибка, возникающая при попытке изменить статус на тот же самый."""
    def __init__(self, status):
        super().__init__()
        self.status = status

    def __str__(self):
        return f"Попытка изменить статус на тот же самый: {self.status}"
    