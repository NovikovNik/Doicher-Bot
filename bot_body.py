import time
import telebot
from user import bulk_insert_new_words_to_db, create_word_object, delete_user_from_db, find_user_in_db, initial_user_create, get_all_chat_ids, add_new_word_to_db, set_word_status
from utils import check_time_for_post, is_time_between
from word_generator import get_sentense
import schedule
import os
import dotenv
from threading import Thread
from repo.bot_repo import get_questions


dotenv.load_dotenv()
token = os.environ.get('TOKEN')
bot = telebot.TeleBot(token)


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
        bot.reply_to(
            message, f"Привет, {username}! Мы с тобой еще на знакомы.")
        initial_user_create(user_name=user_id, nick=username, chat_id=chat)
        bot.send_message(
            chat_id=chat, text="Я Doicher 🇩🇪. Бот, который помогает учить немецкий язык. Я буду отправлять тебе новые немецкие слова каждый день!")
        return
    bot.reply_to(
        message, f"Привет, {username} ты уже зарегестрирован в системе! Если хочешь удалить свои данные выбери пункт 'отписаться' в меню")


@bot.message_handler(commands=['word'])
def get_new_word(message):
    """Отправка картинки и подписи с парой слов вне очереди шедулера.
    """
    chat_id, message_id = message.chat.id, message.id
    word, fword = get_sentense('German.txt', pic=chat_id)
    with open(f'images/pic_{chat_id}.jpg', 'rb') as f:
        bot.send_photo(chat_id=chat_id, photo=f,
                       caption=f'{word}', reply_markup=get_questions())
        # bot.send_poll(chat_id=chat_id,question='choose one',options=['a','b','c'])
        add_new_word_to_db(chat_id=chat_id, word=fword, message_id=message_id)


def send_word_of_the_day():
    if is_time_between(begin_time=(10, 00), end_time=(20, 00)) and check_time_for_post():
        word, f_word = get_sentense('German.txt')
        obj = []
        for i in get_all_chat_ids():
            obj.append(create_word_object(i, f_word, 1))
            message = bot.send_photo(chat_id=i, photo=open(
                'images/day_word.jpg', 'rb'), caption=f"{word}", reply_markup=get_questions())
            print(message.message.id)
        bulk_insert_new_words_to_db(obj)


@bot.message_handler(commands=['stop'])
def get_delete_user(message):
    """Отписка от сервиса.
    """
    user = find_user_in_db(message.from_user.id)
    if not user:
        bot.reply_to(
            message, f"Привет! Мы с тобой еще на знакомы. Напиши /start, чтобы начать погружение в мир немецкого языка.")
        return
    delete_user_from_db(message.from_user.id)
    bot.reply_to(message, f"Отписка от сервиса произведена.")
    return


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat, message_id = call.message.chat.id, call.message.id
    if call.data == "yes":
        bot.send_message(
            chat_id=chat, text='Versuchen Sie es noch einmal, vielleicht werden Sie etwas Neues lernen 😌', reply_to_message_id=message_id)
        set_word_status(id=message_id, status=1)
    elif call.data == "no":
        bot.send_message(chat_id=chat, text='Отлично. Durch Dornen zu den Sternen 🌟',
                         reply_to_message_id=call.message.id)
        set_word_status(id=message_id, status=0)
    bot.edit_message_reply_markup(
        message_id=message_id, reply_markup=None, chat_id=chat)


schedule.every(1).minute.do(send_word_of_the_day)


def start_job():
    while True:
        schedule.run_pending()
        time.sleep(1)
