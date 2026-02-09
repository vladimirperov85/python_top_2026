"""1 Посчитать количество символов,
2 слов,
3 строк,
4 количество пустых и не пустых строк,
5 количество гласных,сагласных,спец символов,
6 статистический анализ букв(частота встречаемости
символов"""
def get_text(path_text_file:str)-> str|None:
    """
    get test from file

    """
    with open(path_text_file, "r", encoding="utf-8") as file:
        text = file.read()
    return text


def get_count_chars(text:str)-> int:
    count_chars =  len(text)
    return count_chars



def get_count_words(text):
    """
    get test from text
    :param text:
    :return:
    """
    words = len(text.split())
    return words




def get_count_lines(text:str)-> dict:
    lines = text.splitlines()
    count_lines = len(lines)
    count_lines_not_empty = 0
    count_empty = 0
    for line in lines:
        if line != "":
            count_lines_not_empty += 1
        elif line == "":
            count_empty += 1
    result = {
        "количество сторок": count_lines,
        "количество не пустых строк": count_lines_not_empty,
        "количество пустых строк": count_empty,
    }
    return result


def get_stat_symbols(text: str) -> dict:
    vowels = 'аеёиоуыэюя'
    consonats = 'бвгджзклмнпрстфхцчшщ'
    spec_symbols = '.,!?-:\'\"%(){}<>;+=*"'
    vowels_count = 0
    consonats_count = 0
    spec_symbols_count = 0

    for symbol in text:
        if symbol.lower() in vowels:
            vowels_count += 1
        elif symbol.lower() in consonats:
            consonats_count += 1
        elif symbol.lower() in spec_symbols:
            spec_symbols_count += 1

    result = {'количество гласных': vowels_count,
              'количество согласных': consonats_count,
              'количество спецсимволов': spec_symbols_count
              }

    return result




def get_character_frequency(text):
    frequency = {}
    for i in text.lower():
        if i in frequency:
            continue
        count = text.lower().count(i)
        frequency[i] = count
    return frequency






# if __name__ == "__main__":


# text_cont = get_text(path_text_file='poem.txt')
# count_chars = get_count_chars(text_cont)
# print('Количество символов:', count_chars)
# count_words =  get_count_words(text_cont)
# print('Количество слов в тексте:', count_words)
# count_lines  = get_count_lines(text_cont)
# print(count_lines)
# stars_symbols = get_stat_symbols(text_cont)
# print(stars_symbols)
# frequency = get_character_frequency(text_cont)
# for key, value in frequency.items():
#     print(key, value)