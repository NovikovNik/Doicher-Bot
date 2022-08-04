from deep_translator import PonsTranslator


def tranlate_word(word):
    translated = PonsTranslator(source='english', target='russian').translate(word, return_all=False)
    return translated