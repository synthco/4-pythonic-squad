from flask import Flask, jsonify, request
from Backend.API.dfender import Dfender
import requests
import json
import datetime

app = Flask(__name__)
# Введіть свій власний токен тут
API_TOKEN = "123"
# Введіть ваш особистий ключ тут
key = "9AJTDWYQN4BA9QE8BD2U3A7QQ"

def get_current_time():
    # Отримати поточний час
    now = datetime.datetime.now()
    # Перетворити час у рядок з форматом 10:00:00
    current_time = now.strftime("%H:%M:%S")
    return current_time

def generate_schedule(location_name):
    # Отримати поточний час
    current_time = get_current_time()
    # Згенерувати розклад для кожної години від 12:00 до 00:00
    schedule = {}
    for hour in range(12, 25):
        hour_str = str(hour % 24).zfill(2) + ":00"  # Обрізати години, щоб залишити формат 00:00
        if hour_str == current_time:
            schedule[hour_str] = True
        else:
            schedule[hour_str] = False
    return {location_name: schedule}

#endpoint
@app.route("/predict", methods=['POST'])
def predict():
    json_data = request.get_json()

    if json_data is None:
        raise InvalidUsage("Request data is missing or not in JSON format", status_code=400)

    # Getting data from JSON doc and creating new variables using it
    requester_name = json_data.get("requester_name")
    locations = json_data.get("locations")

    # Checking if token is correct and is present, checking if other required members are present, etc.
    if locations is None:
        raise InvalidUsage("locations is required fields", status_code=400)

    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    dfender = Dfender()
    info = info_combine(locations, dfender)

    return jsonify(info)


def region_out(n, defender):
    values = defender[n:(n + 11)]
    result = {idx: val for idx, val in enumerate(values)}
    return result


def info_combine(locations, defender):
    deflocations = ["Kyiv", "Rivne", "Lutsk", "Lviv", "Zhytomyr",
                    "Chernivtsi", "Ivano-Frankivsk", "Ternopil", "Khmelnytskyi",
                    "Uzhhorod", "Vinnytsia", "Cherkasy", "Poltava", "Chernihiv",
                    "Sumy", "Kharkiv", "Kropyvnytskyi", "Dnipro", "Mykolaiv",
                    "Kharkiv", "Zaporizhzhia", "Donetsk", "Odesa", "Chernihiv",
                    "Kherson"]

    result = []
    for location in locations:
        if location in deflocations:
            result.append(region_out(deflocations.index(location), defender))
    return result

    #

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>KMA team 4: API Alarms.</h2></p>"

if __name__ == "__main__":
    app.run(debug=True)
