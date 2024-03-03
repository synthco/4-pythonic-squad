import asyncio
import configparser
import datetime
import json

import re

import pytz as pytz
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)

import requests

dict_of_region_names = {"Хмельницька область": "Хмельн",
                        "Вінницька область": "Вінни",
                        "Рівненська область": "Рівн",
                        "Волинська область": "Волин",
                        "Дніпропетровська область": "Дніпро",
                        "Житомирська область": "Житом",
                        "Закарпатська область": "Закарп",
                        "Запорізька область": "Запор",
                        "Івано-Франківська область": "Івано-Франк",
                        "Київська область": "Киї",
                        "Кіровоградська область": "Кіров",
                        "Луганська область": "Луган",
                        "Миколаївська область": "Микола",
                        "Одеська область": "Оде",
                        "Полтавська область": "Полтав",
                        "Сумська область": "Сум",
                        "Тернопільська область": "Терноп",
                        "Харківська область": "Харк",
                        "Херсонська область": "Херс",
                        "Черкаська область": "Черка",
                        "Чернігівська область": "Черніг",
                        "Чернівецька область": "Чернів",
                        "Львівська область": "Львів",
                        "Донецька область": "Доне",
                        "Автономна Республіка Крим": "Крим",
                        "м. Севастополь": "Севастополь",
                        "м. Київ": "Київ"
                        }

uid_dict = {"Хмельницька область": 3,
            "Вінницька область": 4,
            "Рівненська область": 5,
            "Волинська область": 8,
            "Дніпропетровська область": 9,
            "Житомирська область": 10,
            "Закарпатська область": 11,
            "Запорізька область": 12,
            "Івано-Франківська область": 13,
            "Київська область": 14,
            "Кіровоградська область": 15,
            "Луганська область": 16,
            "Миколаївська область": 17,
            "Одеська область": 18,
            "Полтавська область": 19,
            "Сумська область": 20,
            "Тернопільська область": 21,
            "Харківська область": 22,
            "Херсонська область": 23,
            "Черкаська область": 24,
            "Чернігівська область": 25,
            "Чернівецька область": 26,
            "Львівська область": 27,
            "Донецька область": 28,
            "Автономна Республіка Крим": 29,
            "м. Севастополь": 30, "м. Київ": 31
            }

API_KEY = "" # DONT EVER COMMIT WITH API !!!


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self):
        res = dict(self.payload or ())
        res["message"] = self.message
        return res

    def print(self):
        print(self.to_dict())


def get_alarm_by_url(location):
    index = uid_dict.get(location)
    url = f"https://api.alerts.in.ua/v1/iot/active_air_raid_alerts/{index}.json?token={API_KEY}"
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    raise InvalidUsage(response.text, status_code=response.status_code)


# returns true if there is an alarm in region, else, false
def get_alarm(location):
    if location not in uid_dict:
        return InvalidUsage(message=f"Invalid location - {location}").print()
    alarm = get_alarm_by_url(location)
    if alarm == "A":
        return True
    return False


# Creates telegram client, then takes all messages from telegram channel
async def get_day_report(date):
    config = configparser.ConfigParser()
    config.read("config.ini")

    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    api_hash = str(api_hash)
    phone = config['Telegram']['phone']
    username = config['Telegram']['username']

    client = TelegramClient(username, api_id, api_hash)
    await client.start()
#    print("Client Created")

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    iterations = 0

    alarms = await client.get_entity("https://t.me/povitryanatrivogaaa")

    day_alarm_report = []
    async for msg in client.iter_messages(alarms):
        if msg.date < date - datetime.timedelta(days=1):
            break
        day_alarm_report.append(msg.text)

    return day_alarm_report


def get_needed_location_report(location, day_alarm_report):
    details_report = []
    location_indecator = dict_of_region_names.get(location)
    pattern = re.compile(location_indecator, re.IGNORECASE)
    if location == "Кіровоградська область":
        for alarm in day_alarm_report:
            if "Повітряна тривога" in alarm and location_indecator in alarm:
                return details_report
            if pattern in alarm or "Кропив" in alarm or "Х-" in alarm\
                    or "Загроза застосування" in alarm or "Активнiсть тактичної авiації" in alarm:
                details_report.append(alarm)
    else:
        for alarm in day_alarm_report:
            if "Повітряна тривога" in alarm and location_indecator in alarm:
                return details_report
            if location_indecator in alarm or "Х-" in alarm or "Загроза застосування" in alarm or "Активнiсть тактичної авiації" in alarm:
                details_report.append(alarm)

    return details_report


# get report about alarm
def get_alarm_report(location):

    date = datetime.datetime.now(tz=pytz.UTC)

    day_alarm_report = asyncio.run(get_day_report(date))

    location_alarm_report = get_needed_location_report(location, day_alarm_report)

    alarm_report = f"Alarm in {location} \nAlarm details: \n"

    if len(location_alarm_report) == 0:
        alarm_report = alarm_report + f"No alarm info in {location}"
        return alarm_report

    cleared_report = clear_report(location_alarm_report)

    for report in cleared_report:
        alarm_report = alarm_report + "" + report + "\n"

    return alarm_report


# clears all useless symbols
def clear_report(alarm_report):
    cleared_report = []
    for report in alarm_report:
        cleared_message = report.replace('\n', '').replace('*', '')
        cleared_report.append(cleared_message)
    return cleared_report


# Function to print if alarm and its report
def get_text_report(location):
    if not get_alarm(location):
        return f"No alarm in {location}"

    return get_alarm_report(location)


LOCATION = "Харківська область"
print(get_text_report(LOCATION))
