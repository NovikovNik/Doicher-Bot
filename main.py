from random import randint
from translator import tranlate_word

def file_reader(lang):
    i = randint(10, 9730)
    """Чтение файла со списком слов и выбор случайного из них
    """
    with open(lang, 'r', encoding = "ISO-8859-1") as f:
        for _, line in enumerate(f):
            if _ == (i):
                _format_line(line)
                

def _format_line(line):
    """Формиратирование полученной строки. Первое слово - английский вариант,
    второе - немецкий. Отрезается символ новой строки.
    """
    source = line[:-1]
    tmp = source.split('\t')
    pretty_view_string(tmp)
    

def pretty_view_string(words):
    print(f"The word of the day is: {words[1]}, that means: {tranlate_word(words[0])}.")
    
    
file_reader('German.txt')
    