# Doicher Bot - телеграм бот для изучения немецкого языка
____


![logo](images/logo.png)

### Данный бот призван помочь в изучении немецкого языка.    
После авторизации пользователь будет получать сообщение с новым немецким словом и его переводом. Время рассылки настраивается в конфигурационном файле.
Изученные слова сохраняются в базу данных для использования в еженедельной статистике (wip)

Идеей для создания бота поступила цитата, которая сейчас находится в логотипе бота:
> Wer rastet, der rostet

Что дословно можно перевести как - *"Тот, кто ничего не делает, покрывается ржавчиной"*.    
Именно с этой мыслью я приступил к разработке бота - помочь себе в практике немецкого языка, а также попрактиковаться в использовании Python.

**Опробовать бота можно здесь:** [Телеграме](http://t.me/doicher_bot).
____

## Оглавление

0. [Возможности бота](#Возможности-бота)
1. [Что внутри?](#Что-внутри?)
2. [Что в планах?](#Что-в-планах?)
3. [Настройки](#Настройки)

____

## Возможности бота

[![IMG_7730.gif](https://s4.gifyu.com/images/IMG_7730.gif)](https://gifyu.com/image/STmHi)

____

### Регистрация в базе данных бота (Подписка на различные рассылки) ✅    
Чтобы бот отправлял рассылки пользователям они должны быть авторизованы в нём.    
Эта команда добавляет новую запись с указанием ```id пользователя```, ```id чата``` (для добавления в беседы) и ```временной метки``` в таблицу ```USERS```
```
/start
```

### Удаление своих данных из базы данных (Отключение рассылок) ✅
Пользователь удаляется из таблицы ```USERS``` и больше не получает автоматические рассылки от бота.    
Однако пользоваться функциями бота все еще можно, для этого не требуется авторизация в системе.
```
/stop
```

### Получить новое слово с переводом ✅
Если пользователю хочется узнать больше слов то у него для этого есть возможность.    
Команда генерирует случайное слово с переводом и отправляет его пользователю. Отправленное слово сохраняется в таблице ```LEARNED_WORDS``` с указанием ```id``` пользователя и ```timestamp```.
У пользователя также есть возможность отметить было ли известно слово до этого или нет. Эти данные сохраняются в таблице ```WORDS_STATUS```
```
/word
```

### Автоматическая рассылка новых слов✅
Администратор сервера может установить время, в которое пользователям будет отправляться рассылка.    
Сделать это можно в файле ```config.py``` указав время для рассылки в переменной ```hours```
```python
#Пример
hours = (['10', '00'], ['11', '30'], ['12', '30'],
         ['14', '00'], ['17', '00'], ['19', '00'])
```

### Получить статистику по изученным (отправленным) словам ✅
У пользователя есть возможность вывести статистику (в определенных ситуациях она также отправляется автоматически), которая будет включать в себя следующие пункты:
* Суммарное время взаимодействия с ботом (Когда пользователь авторизовался) в формате dd-mm-yyyy
* Общее количество полученых слов
* Количество слов со статусом - **"Известное"**
* Количество слов со статусом - **"Неизвестное"**

У администратора есть возможность **построить график** по полученной статистике.
<details>
  <summary> Построение графиков статистики</summary>
  
  Имеется базовый функционал создания графиков статистики. На данный момент можно построить график по количеству реакций на полученные слова.
  Чтобы это сделать, необходимо вызвать метод ```generate_graph()``` модуля ```graphics.py``` без дополнительных аргументов.

  В ответе будет сгенерирован график в папке ```images/graph.png```
  
![graph](images/graph_ex.png)
  
</details>
<br>

```python
#Различные команды для вызова статистики
/stat, /stats, /statistics
```
____

## Что внутри?

### Бот написан с использованием:

* **pyTelegramBotAPI** -- отвечает за взаимодействие с Api телеграм
* **SQLAlchemy** -- общение и создание базы данных. В примере используется SQLite
* **Pillow** -- для генерации текста с переводами фраз на изображениях
* **deep-translator** -- для перевода слов с немецкого на русский. Используется Google Translate
* **TypeGuard** -- для разного TypeHinting. Этот момент все еще дорабатывается и есть не везде
* **shedule** -- отвечает за запуск заданий на рассылку по расписанию
* **matplotlib** -- для построения графиков

____

## Что в планах?

На данный момент еще не реализованы, но планируется:

* Сбор различной статистики по запросам и новым пользователям
* Вывод еженедельной статистики по изученным словам
* Возможность отправлять и настраивать кастомные сообщения
* Улучшения работы с базой данных
* Логирование действий бота
* Тесты на базовые функции

____

## Настройки

В репозитории имеется Dockerfile. С помощью него можно собрать локально образ бота.
```
cd Doicher-Bot &&
docker build --tag doicher-bot .
```

Также можно запустить через docker-compose (3.3). В таком случае база данных прикрепляется как отдельный volume.
```
volumes:
    - /home/nick/media-server/database:/app/database/
```

Запуск осуществляется через:
```
docker-compose up -d
```