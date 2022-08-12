from telebot import types

hideBoard = types.ReplyKeyboardRemove()


def get_questions() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👍🏻 Уже знал(а)", callback_data="yes"),
                               types.InlineKeyboardButton("👎🏻 Не знал(а)", callback_data="no"))
    return markup