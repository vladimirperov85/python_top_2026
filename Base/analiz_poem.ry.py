from text_utils import*
from os.path import isfile

while True:
    print('Введите имя файла для анализа:')
    print('Введите 0 для выхода:')
    path = input('>>> ')

    if path == '0':
        print('Выход из программы')
        break  # Этот break находится внутри цикла while - правильно

    if isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        break  # Этот break выходит из цикла ввода имени файла после успешного чтения
    else:
        print('Такого файла нет')
        # Здесь НЕТ break, поэтому цикл продолжается и просит ввести имя файла снова

while True:
    print('Выбрать необходимое действие')
    print('1. Посчитать количество строк в файле\n'
          '2. Посчитать количество слов в файле\n'
          '3. Посчитать количество символов в файле\n')

    action = input('>>> ')

    match action:
        case '1':
                print('Посчитать количество строк в файле')
                lines = get_count_lines(text)
                print(lines)

        case '2':
                print('Посчитать количество слов в файле')
                words = get_count_words(text)
                print(words)

        case '3':
                print('Посчитать количество символов в файле')
                characters = get_character_frequency(text)
                print(characters)

        case _:
                print('Неверный ввод')


