from models import LibraryManager


if __name__ == "__main__":
    manager = LibraryManager("sqlite:///BD_home_work/My_bd.db")
    manager.create_tables()
    
    # 1. Реализовать поиск книг по автору и отображение списка книг с именами авторов.
    # 1.1. В LibraryManager добавьте метод find_books_by_author_name(self, author_name).
    # Используйте join между таблицами Book и Author, чтобы найти книги, связанные с
    # автором, имя которого совпадает с author_name.
    # 1.2. В LibraryManager добавьте метод display_all_books_with_authors(self). Также
    # используйте join, чтобы получить список книг вместе с именами их авторов и красиво
    # выведите эту информацию в консоль.
    # 1.3. В main.py протестируйте оба новых метода.
        
    # Выводим все книги с авторами
    # print("Все книги в библиотеке:")
    # print("-" * 40)
    # manager.display_all_books_with_authors()
    
    
    # author_name = "Ваше имя автора"
    # print(f"Книги автора: {author_name}")
    # print("-" * 40)
    # books = manager.find_books_by_author_name(author_name)
    # if books:
    #     for book in books:
    #         print(f" \"{book.title}\" ({book.year})")
    # else:
    #     print("Книги не найдены.")
    
    
    # 2. Добавить проверки зависимостей при удалении и реализовать обработку ошибок.
    # 2.1. Обновите метод delete_author в LibraryManager. Перед удалением проверьте, есть ли у
    # автора книги в базе. Если есть, вызовите исключение (например, ValueError) с
    # понятным сообщением.
    # 2.2. Обновите метод delete_book в LibraryManager. Перед удалением проверьте, выдана ли
    # книга кому-то (есть ли активная запись BookIssue). Если да, вызовите исключение.
    # 2.3. Обновите метод delete_reader в LibraryManager. Перед удалением проверьте, есть ли у
    # читателя активные (не возвращённые) книги. Если да, вызовите исключение.
    # 2.4. В main.py протестируйте эти случаи и убедитесь, что исключения выбрасываются
    # правильно.
    
    
    # Выдадим книгу
    # print("Выдаём книгу читателю")
    # issue = manager.issue_book_to_reader(1,1)
    # print(f"Пытаемся удалить книгу {1}, которая выдана:")
    # try:
    #     manager.delete_book(1)
    # except ValueError as e:
    #     print(f"Ожидаемое  исключение: {e}")
    
    # Попробуем удалить читателя
    # print(f"Пытаемся удалить читателя {1}, у которого есть книга:")
    # try:
    #     manager.delete_reader(1)
    # except ValueError as e:
    #     print(f"Ожидалось исключение: {e}")
    
    # Попробуем удалить автора, вначале посмотрим книги у него
    # books = manager.find_books_by_author_name("Здесь ваш автор")
    # print(f"Найдено книг у автора: {len(books)}")
    # print(f"Пытаемся удалить автора {1}, у которого есть книги:")
    # try:
    #     manager.delete_author(1)
    # except ValueError as e:
    #     print(f"Ожидалось исключение: {e}")