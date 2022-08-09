from deep_translator import PonsTranslator, GoogleTranslator


def tranlate_word(word):
    translated = GoogleTranslator(source='english', target='russian').translate(word, return_all=False)
    return translated