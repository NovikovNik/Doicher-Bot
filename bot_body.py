from datetime import datetime
import time
import telebot
from user import bulk_insert_new_words_to_db, create_word_object, delete_user_from_db, find_user_in_db, get_user_stats, get_words_amount, initial_user_create, get_all_chat_ids, add_new_word_to_db, set_word_status, Data
from utils import check_time_for_post, is_time_between
from word_generator import get_sentense
import schedule
import os
import dotenv
from threading import Thread
from repo.bot_repo import get_questions
import logging
import config
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, Counter, Info


dotenv.load_dotenv()
token = os.environ.get('TOKEN')
bot = telebot.TeleBot(token)


logging.basicConfig(filename='log',
                    filemode='a', 
                    level=logging.INFO, 
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


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
            chat_id=chat, text=f"Я Doicher 🇩🇪. Бот, который помогает учить немецкий язык. Я буду отправлять тебе новые немецкие слова каждый день!")
        logger.info("New user")
        return
    bot.reply_to(
        message, f"Привет, {username} ты уже зарегестрирован в системе! Если хочешь удалить свои данные выбери пункт 'Остановить рассылку' в меню")
    send_word_of_the_day()


@bot.message_handler(commands=['word'])
def get_new_word(message):
    """Отправка картинки и подписи с парой слов вне очереди шедулера.
    """
    chat_id, message_id = message.chat.id, message.id
    word, fword = get_sentense('German.txt', pic=chat_id)
    with open(f'images/pic_{chat_id}.jpg', 'rb') as f:
        message = bot.send_photo(chat_id=chat_id, photo=f,
                                 caption=f'{word}', reply_markup=get_questions(), parse_mode='MarkdownV2')
        # bot.send_poll(chat_id=chat_id,question='choose one',options=['a','b','c'])
        add_new_word_to_db(chat_id=chat_id, word=fword, message_id=message.id)
        logger.info("User get new word")
        # config.words_per_session= config.words_per_session+1
        # print(config.words_per_session)
        registry = CollectorRegistry()
        g = Counter('words_count_job', 'User successfully get new word', registry=registry)
        g.inc(int(get_words_amount()))
        push_to_gateway('prom:9091', job='doicher', registry=registry)


def send_word_of_the_day():
    if is_time_between(begin_time=(10, 00), end_time=(20, 00)) and check_time_for_post():
        word, f_word = get_sentense('German.txt')
        obj = []
        for i in get_all_chat_ids():
            message = bot.send_photo(chat_id=i, photo=open(
                'images/day_word.jpg', 'rb'), caption=f"{word}", reply_markup=get_questions(), parse_mode='MarkdownV2')
            obj.append(create_word_object(i, f_word, message.id))
            logger.info("User get new word")
            # registry = CollectorRegistry()
            # g = Gauge('day_send_word', 'User successfully get new word', registry=registry)
            # g.inc(1)
        # push_to_gateway('prom:9091', job='doicher', registry=registry)
        bulk_insert_new_words_to_db(obj)


def send_statistic():
    if datetime.today().weekday() == 4:  # Пятница
        for i in get_all_chat_ids():
            stat = get_user_stats(user_id=i, week=True)
            bot.send_photo(
                chat_id=i, photo=open(
                    'images/logo.png', 'rb'), caption=f"""Я собрал для тебя некоторую статистику за прошедшие 7 дней с {stat.get(Data.last_week)} 😺: \n
        Cлов получено: *{stat.get(Data.all_words)}*\n
        Из них:
        Известных тебе: *{stat.get(Data.know_words)}*
        Неизвестных: *{stat.get(Data.unknown_words)}*\n
        Ты подписчик с: *{stat.get(Data.since)}* ❤️""", parse_mode='MarkdownV2')


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
        # registry = CollectorRegistry()
        # g = Gauge('known_job', 'User dosnt know word', registry=registry)
        # g.inc(1)
        # push_to_gateway('prom:9091', job='doicher', registry=registry)
    elif call.data == "no":
        bot.send_message(chat_id=chat, text='Отлично. Durch Dornen zu den Sternen 🌟',
                         reply_to_message_id=call.message.id)
        set_word_status(id=message_id, status=0)
        registry = CollectorRegistry()
        # g = Gauge('not_known_job', 'User dosnt know word', registry=registry)
        # g.inc(1)
        # push_to_gateway('prom:9091', job='doicher', registry=registry)
    bot.edit_message_reply_markup(
        message_id=message_id, reply_markup=None, chat_id=chat)


@bot.message_handler(commands=['stat', 'stats', 'statistics'])
def stats(message):
    if find_user_in_db(message.from_user.id):
        stat = get_user_stats(message.from_user.id, week=True)
        bot.send_photo(
            chat_id=message.chat.id, photo=open(
                'images/logo.png', 'rb'), caption=f"""Я собрал для тебя некоторую статистику за прошедшие 7 дней с {stat.get(Data.last_week)} 😺: \n
Cлов получено: *{stat.get(Data.all_words)}*\n
Из них:
Известных тебе: *{stat.get(Data.know_words)}*
Неизвестных: *{stat.get(Data.unknown_words)}*\n
Ты подписчик с: *{stat.get(Data.since)}* ❤️""", parse_mode='MarkdownV2')


schedule.every(1).minute.do(send_word_of_the_day)
schedule.every().day.at("09:30").do(send_statistic)


def start_job():
    while True:
        schedule.run_pending()
        time.sleep(1)
