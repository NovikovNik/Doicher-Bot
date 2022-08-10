from random import randint
from typing import Callable
from translator import tranlate_word
from pictures import draw_text


def _get_words_from_list(lang: str) -> str:
    i = randint(10, 9730)
    """Чтение файла со списком слов и выбор случайного из них
    """
    with open(lang, 'r', encoding = "ISO-8859-1") as f:
        for _, line in enumerate(f):
            if _ == (i):
                return line
                

def _format_line(line: Callable[[str], list]) -> list:
    """Формиратирование полученной строки. Первое слово - английский вариант,
    второе - немецкий. Отрезается символ новой строки.
    """
    source = line[:-1]
    tmp = source.split('\t')
    return tmp
    

def get_sentense(lang:str, pic=None) -> str:
    """_summary_
        Получение готового к отправке предложения со словом и его переводом.
    Args:
        lang (str): языковой файл
        pic (_type_, optional): Если не указан, создается изображение day_word.jpg, если указан, то
        пользовательское изображение индивидуальное.
    """
    words = _format_line(_get_words_from_list(lang))
    bottom_word = tranlate_word(words[0])
    draw_text(upper=words[1], bottom=bottom_word, user=pic)
    return(f"🇩🇪 Новое слово для тебя: {words[1]}, оно означает: {tranlate_word(words[0])} 🇷🇺")

