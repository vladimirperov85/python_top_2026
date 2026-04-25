from models import LibraryManager


if __name__ == "__main__":
    manager = LibraryManager("sqlite:///BD_home_work/My_bd.db")
    manager.create_tables()
    # # выдаем книги читателям
    print("Выдача книг читателям:")
    print("============================================================")
    manager.issue_book_to_reader(book_id=1, reader_id=1)  # используйте ваши аргументы
    manager.issue_book_to_reader(book_id=2, reader_id=2)
    # # пытаемся выдать книгу которая уже выдана
    manager.issue_book_to_reader(book_id=1, reader_id=1)
    # # пытаемся выдать книгу которой нет в библиотеке
    manager.issue_book_to_reader(book_id=99, reader_id=1)

    # тестирование выдачи книг,её возврат,отображение активных выдач
    print("Активные выдачи:")
    print("============================================================")

    active_after = manager.get_active_issues()  # выводим активные выдачи
    print(active_after)
    print()
    manager.return_book_from_reader(issue_id=1)  # используйте ваши аргументы
    manager.return_book_from_reader(issue_id=3)
    print()
    active_after = manager.get_active_issues()  # выводим активные выдачи после возврата
    print(active_after)
