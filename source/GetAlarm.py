import json
import requests

API_KEY = " " #DONT EVER COMMIT WITH API !!!

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
            "м. Севастополь": 30,
            "м. Київ": 31
            }


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
    else:
        raise InvalidUsage(response.text, status_code=response.status_code)


def get_alarm(location):
    if location not in uid_dict.values():
        return InvalidUsage(message=f"Invalid location - {location}").print()
    alarm = get_alarm_by_url(location)
    if alarm == "A":
        return True
    else:
        return False


loc = "м. Київ"
print(get_alarm(loc))
