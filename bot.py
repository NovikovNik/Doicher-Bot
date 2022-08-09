import time
import telebot
from user import find_user_in_db, initial_user_create, get_all_chat_ids
from word_generator import get_words_from_list
import schedule
import os
import dotenv


dotenv.load_dotenv()
token = os.environ.get('TOKEN')
print(token)
bot = telebot.TeleBot(token)
start_sending = False


def start_pooling():
    bot.infinity_polling()
    start_sending = True


@bot.message_handler(commands=['start'])
def initialising(message):
    word = get_words_from_list('German.txt')
    chat = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.first_name
    user = find_user_in_db(user_id)
    if not user:
        bot.reply_to(message, f"Привет, {username}! Мы с тобой еще на знакомы.")
        initial_user_create(user_name=user_id, nick=username, chat_id=chat)
        bot.send_message(chat_id=chat, text="Добавил тебя в свою базу данных!")
        bot.send_message(chat_id=chat, text=f"{word}")
        return
    bot.reply_to(message, f"Привет, {username} ты уже зарегестрирован в системе! Если хочешь удалить свои данные, перейди в настройки!")
    bot.send_message(chat_id=chat, text=f"{word}")
    

def send_word():
    word = get_words_from_list('German.txt')
    print('do')
    for i in get_all_chat_ids():
        bot.send_message(chat_id=i, text=f"{word}")
        

schedule.every(1).hours.do(send_word)
while start_sending:
    schedule.run_pending()
    time.sleep(1)

