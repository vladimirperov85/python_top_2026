from models import LibraryManager


if __name__ == "__main__":
    manager = LibraryManager("sqlite:///ваш путь к базе данных")
    manager.create_tables()
    # manager.add_author("Bаше имя автора")
    # manager.add_author("Bаше имя автора")
    # manager.add_author("Bаше имя автора")
    # authors = manager.get_all_authors()
    # for author in authors:
    #     print(author.name)
    # author = manager.find_author_by_id(ваш id автора)
    # print(author)
    # update_author = manager.update_author(id-автора, "Новое имя автора")
    # authors_update = manager.get_all_authors()
    # for author in authors_update:
    #     print(author.name)
    pass
