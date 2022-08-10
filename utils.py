from datetime import datetime, time
import pytz


def is_time_between(begin_time, end_time, check_time=None):
    # Спасибо stackoverflow. Эту портянку надо будет переделать. Добавил преобразование
    #чтобы не тащить time в модуль bot
    begin = time(begin_time[0], begin_time[1])
    end = time(end_time[0], end_time[1])
    check_time = check_time or datetime.now(pytz.timezone('Europe/Moscow')).time()
    if begin < end:
        return check_time >= begin and check_time <= end
    else: 
        return check_time >= begin or check_time <= end
    
    