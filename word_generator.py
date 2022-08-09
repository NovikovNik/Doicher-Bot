from random import randint
from translator import tranlate_word


def get_words_from_list(lang):
    i = randint(10, 9730)
    """Чтение файла со списком слов и выбор случайного из них
    """
    with open(lang, 'r', encoding = "ISO-8859-1") as f:
        for _, line in enumerate(f):
            if _ == (i):
                return _format_line(line)
                

def _format_line(line):
    """Формиратирование полученной строки. Первое слово - английский вариант,
    второе - немецкий. Отрезается символ новой строки.
    """
    source = line[:-1]
    tmp = source.split('\t')
    return pretty_view_string(tmp)
    

def pretty_view_string(words):
    return(f"Новое слово для тебя: {words[1]}, оно означает: {tranlate_word(words[0])}")

