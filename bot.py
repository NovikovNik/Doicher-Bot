import time
import telebot
from user import find_user_in_db, initial_user_create, get_all_chat_ids
from word_generator import get_sentense
import schedule
import os
import dotenv
from threading import Thread


dotenv.load_dotenv()
token = os.environ.get('TOKEN')
print(token)
bot = telebot.TeleBot(token)
start_sending = False


def start_pooling():
    """Запуск двух тредов, чтобы шедулер отправки сообщений работал корректно.
    """
    Thread(target=bot.infinity_polling).start()
    Thread(target=start_job).start()


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
        return
    bot.reply_to(message, f"Привет, {username} ты уже зарегестрирован в системе! Если хочешь удалить свои данные, перейди в настройки!")
    send_word_of_the_day()
    
    
@bot.message_handler(commands=['word'])
def get_new_word(message):
    """Отправка картинки и подписи с парой слов вне очереди шедулера.
    """
    chat_id = message.chat.id
    word = get_sentense('German.txt', pic=chat_id)
    with open(f'images/pic_{chat_id}.jpg', 'rb') as f:
        bot.send_photo(chat_id=chat_id, photo=f)
        bot.send_message(chat_id=chat_id, text=f"{word}")
    
    

def send_word_of_the_day():
    word = get_sentense('German.txt')
    img = open('images/day_word.jpg', 'rb')
    for i in get_all_chat_ids():
        bot.send_photo(chat_id=i, photo=img)
        bot.send_message(chat_id=i, text=f"{word}")
        

schedule.every(1).hours.do(send_word_of_the_day)


def start_job():
    while True:
        schedule.run_pending()
        time.sleep(1)
