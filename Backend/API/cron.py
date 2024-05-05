import pandas as pd
from alarms import *
from dfender import Dfender
import pickle
import datetime
import time

df = pd.read_csv("predictions.csv")

dfender = Dfender()
vector = dfender.result

city_id_map = [
        'date',
        'hour_datetime',
        'Vinnytsia',
        'Lutsk',
        'Dnipro',
        'Donetsk',
        'Zhytomyr',
        'Uzhhorod',
        'Zaporizhzhia',
        'Ivano-Frankivsk',
        'Kyiv',
        'Kropyvnytskyi',
        'Lviv',
        'Mykolaiv',
        'Odesa',
        'Poltava',
        'Rivne',
        'Sumy',
        'Ternopil',
        'Kharkiv',
        'Kherson',
        'Khmelnytskyi Oblast',
        'Cherkasy',
        'Chernivtsi',
        'Chernihiv',
        'last_updated'
    ]

now = datetime.datetime.now()
date = now.date()
hour_time = now.replace(minute=0, second=0)


for i, city in enumerate(df.columns[2:-1]):
    if i == 8 or i == 15:
        time.sleep(60)
    start_index = i * 12
    end_index = start_index + 12
    is_alarm = alarms_for_now(i)
    df[city] = vector[start_index:end_index]
    if is_alarm:
        df[city].loc[0] = 1488

df['last_updated'] = now

for i in range(len(df)):
    df.at[i, 'hour_datetime'] = hour_time.strftime("%H:%M:%S")
    if hour_time.hour == 0:
        date += datetime.timedelta(days=1)
    df.at[i, 'date'] = date
    hour_time += datetime.timedelta(hours=1)

print(date, hour_time)

df.to_csv('predictions.csv', index=False)
