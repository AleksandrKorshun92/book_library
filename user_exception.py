class BookError(Exception):
    """Базовый класс для всех ошибок, связанных с книгами."""
    pass

class InvalidBookIDError(BookError):
    """Ошибка, возникающая при передаче неверного ID книги."""
    def __init__(self, book_id):
        super().__init__()
        self.book_id = book_id

    def __str__(self):
        return f"Книга не найдена c id - {self.book_id}"

class DisplayBookError(BookError):
    """Ошибка, возникающая при загрузки книг из библиотеки."""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Библиотека пустая (надо скачать больше книг)"

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
    