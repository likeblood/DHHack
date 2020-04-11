import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from natasha import NamesExtractor
from rutermextract import TermExtractor
import rutermextract
from stop_words import get_stop_words


term_ex = TermExtractor()
names_ex = NamesExtractor()
stop_words = get_stop_words('russian')


def sort_of_list_by_count(lst):
    d = {}
    for word in lst:
        d[word] = 1 if word not in d.keys() else d[word]+1
    sortedD = sorted(d.items(), key=lambda x: x[1], reverse=True)
    
    return [x[0] for x in sortedD]


def data_to_text(data):
    text_serie = data['text'].dropna()
    text_serie.apply(lambda x: x.rstrip())
    text = text_serie.to_string()
    # text.lower()
    regex = re.compile('[^а-яА-я]')
    text = regex.sub(' ', text)
    text = re.sub(" +", " ", text)

    reply_text_serie = data['reply.text'].dropna()
    reply_text_serie.apply(lambda x: x.rstrip())
    reply_text = reply_text_serie.to_string()
    reply_text.lower()
    regex = re.compile('[^а-яА-я]')
    reply_text = regex.sub(' ', reply_text)
    reply_text = re.sub(" +", " ", reply_text)

    return reply_text + text


def exclude_stop_words(text):
    words = []
    for word in text.split():
        if not(word in stop_words):
            words.append(word)
    return ' '.join(words)


def text_analize(path):
    date = str(path[-14:-4])
    if path[-23] == 's':
        data = pd.read_csv("/Users/ba/Documents/DHhack/getting_data/soloviev.csv", index_col=0)
    else:
        data = pd.read_csv('/Users/ba/Documents/DHhack/getting_data/navalny.csv', index_col=0)
    data['Date'] = data['Date'].apply(lambda x: x.split()[0])
    text = data_to_text(pd.read_csv(path, index_col=0))
    terms, names = [], []
    text = exclude_stop_words(text)
    for term in term_ex(text, limit=6):
        terms.append((term.normalized, term.count))
    for match in names_ex(text):
        name = '{} {} {}'.format(match.fact.first, match.fact.middle, match.fact.last)
        name = name.replace('None', '')
        name = name.lstrip()
        names.append(name)
    names = set(names)
    return [date, float(data[(data['Date'] == date) & (data['Comments'] > 2400)]['Likes']),\
            float(data[(data['Date'] == date) & (data['Comments'] > 2400)]['Dislikes']), \
            float(data[(data['Date'] == date) & (data['Comments'] > 2400)]['Comments']), \
            float(data[(data['Date'] == date) & (data['Comments'] > 2400)]['Views']), terms, \
            sort_of_list_by_count(names)[0:10]]


def make_full_statistic_by_videos(videos):
    lst = []
    for video in videos:
        lst.append(text_analize(video))
    return lst


def make_df(info):
    dates, likes, dislikes, comments, views, key_words, names = [], [], [], [], [], [], []
    for i in range(len(info)):
        dates.append(info[i][0])
        likes.append(info[i][1])
        dislikes.append(info[i][2])
        comments.append(info[i][3])
        views.append(info[i][4])
        key_words.append(info[i][5])
        names.append(info[i][6])
    return pd.DataFrame({
                    "dates": dates,
                    "likes": likes,
                    "dislikes": dislikes,
                    "comments": comments,
                    "views": views,
                    "key words": key_words,
                    "propr names": names
                        })


soloviev_videos = ['/Users/ba/Documents/DHhack/data_preprocessing/soloviev/soloviev_2019-07-29.csv',\
                    '/Users/ba/Documents/DHhack/data_preprocessing/soloviev/soloviev_2019-08-05.csv',\
                    '/Users/ba/Documents/DHhack/data_preprocessing/soloviev/soloviev_2019-08-26.csv',\
                    '/Users/ba/Documents/DHhack/data_preprocessing/soloviev/soloviev_2019-08-28.csv']
navalny_videos = ['/Users/ba/Documents/DHhack/data_preprocessing/navalny/navalny_2019-07-01.csv',\
                 '/Users/ba/Documents/DHhack/data_preprocessing/navalny/navalny_2019-07-18.csv',\
                 '/Users/ba/Documents/DHhack/data_preprocessing/navalny/navalny_2019-08-01.csv']

soloviev_info = make_full_statistic_by_videos(soloviev_videos)
navalny_info = make_full_statistic_by_videos(navalny_videos)

soloviev_df = make_df(soloviev_info)
navalny_df = make_df(navalny_info)

soloviev_df.to_csv("soloviev_info.csv")
navalny_df.to_csv("navalny_info.csv")
