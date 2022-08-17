from typing import Dict
import models
from database import get_db
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sqlalchemy import or_
from dataclasses import dataclass

db = get_db()


def _get_stats_for_seven_day():
    with db.begin() as session:
        data = {'all_words': session.query(models.Words).count(),
                'know_words': session.query(models.Words.time_stamp)
                .filter(or_(models.WordsStatus.status == 1, models.WordsStatus.status == 0))
                .filter(models.WordsStatus.word_id == models.Words.id)
                .filter(models.Words.time_stamp >= (datetime.now() - timedelta(weeks=1))).all(),
                'unknow_words': session.query(models.Words, models.WordsStatus)
                .filter(models.WordsStatus.status == 0)
                .filter(models.WordsStatus.word_id == models.Words.id).distinct().count()
                }
        return data

@dataclass
class Data():
    know_words = 'know_words'
    unknown_words = 'unknow_words'
    all_words = 'all_words'
    

def _get_count(stats, source: Data) -> Dict:
    data = {}
    for i in stats.get(source):
        for j in i:
            print(j)
            if j.strftime("%m %d %Y") not in data:
                data.update({(j.strftime("%m %d %Y")): 1})
            else:
                data.update({j.strftime("%m %d %Y"): int(
                    data.get(j.strftime("%m %d %Y"))+1)})
    return data


def generate_graph():
    tmp = _get_stats_for_seven_day()
    result = _get_count(tmp, source=Data.know_words)
    ax = plt.subplot()
    x, y = zip(*sorted(result.items()))
    ax.plot(x, y, label="Реакции общие")
    ax.plot(x, y, label="Реакции общие")
    ax.set_xlabel("7 прошедших дней")
    ax.set_ylabel("Количество реакций")
    ax.set_title(
        f"Реакции на слова за прошедшие 7 дней (c {(datetime.now() - timedelta(weeks=1))})")
    plt.savefig('images/graph.png')
    
