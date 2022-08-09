import telebot
from user import find_user_in_db, initial_user_create
from word_generator import get_words_from_list
import os
import dotenv


dotenv.load_dotenv()
token = os.environ.get('TOKEN')
print(token)
bot = telebot.TeleBot(token)


def start_pooling():
    bot.infinity_polling()


@bot.message_handler(commands=['start'])
def initialising(message):
    chat = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.first_name
    user = find_user_in_db(user_id)
    if not user:
        bot.reply_to(message, f"Привет, {username}! Мы с тобой еще на знакомы.")
        initial_user_create(user_name=user_id, nick=username, chat_id=chat)
        bot.send_message(chat_id=chat, text="Добавил тебя в свою базу данных!")
        bot.send_message(chat_id=chat, text=f"{get_words_from_list('German.txt')}")
        return
    bot.reply_to(message, f"Привет, {username} ты уже зарегестрирован в системе! Если хочешь удалить свои данные, перейди в настройки!")