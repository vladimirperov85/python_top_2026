from models import LibraryManager


if __name__ == "__main__":
    manager = LibraryManager("sqlite:///BD_home_work/My_bd.db")
    manager.create_tables()

    # Код для  тестирования методов сущности Book

    manager.add_book(title="Война и мир", author_id=1, year=1869, isbn="1234567890")
    author = manager.add_author("Лев Толстой")
    print()
    # Добавим книгу с существующим author_id
    book = manager.add_book(title="Война и мир", author_id=author.id, year=1869)
    print()
    # Получим все книги
    all_books = manager.get_all_books()
    for b in all_books:
        print(b)
    print()
    # Найдём книгу по ID
    found_book = manager.find_book_by_id("id книги из вашей базы данных")
    if found_book:
        print(f"Найдена: {found_book}")
    else:
        print("Книга не найдена.")
    print()
    # Обновим название книги
    manager.update_book(
        book_id="id книги из вашей базы данных",
        new_title="Новое название  книги",
        new_year="новый год выпуска книги",
    )
    updated_book = manager.find_book_by_id("id книги из вашей базы данных")
    print()
    # Удалим книгу
    manager.delete_book("id книги из вашей базы данных")
    print()
    # Код для  тестирования методов сущности Reader

    reader1 = manager.add_reader("Иван", "Петров", "ivan@example.com")
    print()
    manager.update_reader(2, new_email="новый email")
    print()
    manager.update_reader(2, new_first_name="новое имя")
    print()
    manager.delete_reader(2)
    print()
