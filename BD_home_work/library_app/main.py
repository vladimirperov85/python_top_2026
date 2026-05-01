from models import LibraryManager


def main():
    manager = LibraryManager("sqlite:///BD_home_work/My_bd.db")
    manager.create_tables()
    while True:
        print("\n=== Меню Библиотеки ===")
        print("1. Добавить автора")
        print("2. Добавить книгу")
        print("3. Выдать книгу читателю")
        print("4. Принять книгу обратно")
        print("5. Показать активные выдачи")
        print("6. Показать все книги с авторами")
        print("7. Найти книги по имени автора")
        print("8. Добавить читателя")
        print("0. Выйти")
        print("------------------------")

        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("До свидания!")
            break
        elif choice == "1":
            name = input("Введите имя автора: ").strip()
            if not name:
                print("Имя автора не может быть пустым.")
                continue
            try:
                manager.add_author(name)
            except Exception as e:
                print(f"Ошибка при добавлении автора: {e}")
        elif choice == "8":
            # Добавление читателя
            first_name = input("Введите имя читателя: ").strip()
            last_name = input("Введите фамилию читателя: ").strip()
            email = input("Введите email читателя: ").strip()

            if not first_name or not last_name or not email:
                print("Имя, фамилия и email не могут быть пустыми.")
                continue

            try:
                manager.add_reader(first_name, last_name, email)
            except Exception as e:
                print(f"Ошибка при добавлении читателя: {e}")
        elif choice == "2":
            # Добавление книги
            title = input("Введите название книги: ").strip()
            author_id = input("Введите id автора: ").strip()
            year = input("Введите год издания книги: ").strip()
            isbn = input("Введите ISBN книги: ").strip()

            if not title or not author_id or not year or not isbn:
                print(
                    "Название книги, id-автора,год или индивидуальный номер книги не могут быть пустыми."
                )
                continue
            try:
                manager.add_book(title, author_id, year, isbn)
            except Exception as e:
                print(f"Ошибка при добавлении книги: {e}")
        elif choice == "3":
            # Выдача книги читателю
            try:
                book_id = int(input("Введите ID книги: ").strip())
                reader_id = int(input("Введите ID читателя: ").strip())
                manager.issue_book_to_reader(book_id, reader_id)
            except Exception as e:
                print(f"Ошибка при выдаче книги: {e}")
        elif choice == "4":
            # Принять книгу обратно
            try:
                issue_id = int(input("Введите ID выдачи: ").strip())
                manager.return_book_from_reader(issue_id)
            except Exception as e:
                print(f"Ошибка при возврате книги: {e}")
        elif choice == "5":
            # Показать активные выдачи
            try:
                issues = manager.get_active_issues()
                for issue in issues:
                    print(issue)
            except Exception as e:
                print(f"Ошибка при получении активных выдач: {e}")
        elif choice == "6":
            # Показать все книги с авторами
            try:
                manager.display_all_books_with_authors()
            except Exception as e:
                print(f"Ошибка при получении книг: {e}")
        elif choice == "7":
            # Найти книги по имени автора
            try:
                author_name = input("Введите имя автора: ").strip()
                books = manager.find_books_by_author_name(author_name)
                for book in books:
                    print(book)
            except Exception as e:
                print(f"Ошибка при поиске книг: {e}")


if __name__ == "__main__":
    main()
