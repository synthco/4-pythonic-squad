import requests
import pandas as pd
import csv
from datetime import datetime, timedelta

current_date = datetime.now()
one_day_delta = timedelta(days=1)
next_day = current_date + one_day_delta
date = next_day.strftime("%Y-%m-%d")

key = "RCWWMPLADXCCSTWC9Q6KCL9PG"
locations = ["Kyiv", "Rivne", "Lutsk", "Lviv", "Zhytomyr",
             "Chernivtsi", "Ivano-Frankivsk", "Ternopil", "Khmelnytskyi",
             "Uzhhorod", "Vinnytsia", "Cherkasy", "Poltava", "Chernihiv",
             "Sumy", "Kharkiv", "Kropyvnytskyi", "Dnipro", "Mykolaiv",
             "Kharkiv", "Luhansk", "Donetsk", "Odesa", "Chernihiv",
             "Kherson"]


def json_to_csv(key, location, date, output_file="weather_daily_set.csv"):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location},Ukraine/{date}?key={key}"

    response = requests.get(url)
    data = response.json()

    if 'days' in data:
        with open(output_file, "w", newline="", encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            others = {key: data[key] for key in
                      ['latitude', 'longitude', 'resolvedAddress', 'address', 'timezone', 'tzoffset']}
            day_data = data['days'][0]
            hourly_data = day_data.get('hours', [])
            daily_keys = set(day_data.keys())
            hourly_keys = set()
            for hour in hourly_data:
                hourly_keys.update(hour.keys())
            all_keys = list(others.keys()) + list(daily_keys) + list(hourly_keys)
            writer.writerow(all_keys)

            for day in data['days']:
                day_values = [day.get(key, "") for key in daily_keys]
                for hour in day["hours"]:
                    hourly_values = [hour.get(key, "") for key in hourly_keys]
                    row = [others.get(key, "") for key in others.keys()] + day_values + hourly_values
                    writer.writerow(row)

        print(f"Data has been written to {output_file}")

    return "weather_daily_set.csv"



# %%
def to_celsius(x):
    return (x - 32) * (5 / 9)


def clear_df(location, key, date):
    file = json_to_csv(key, location, date)
    df = pd.read_csv(file)
    df.drop(["hours"], axis=1, inplace=True)
    columns_to_convert = ['tempmax', 'temp', 'tempmin', 'feelslike', 'feelslikemax', 'feelslikemin']
    df[columns_to_convert] = df[columns_to_convert].map(lambda x: (x - 32) * (5 / 9))
    df.fillna(0, inplace=True)
    return df.head(12)


def df_csv(df, f_name='weather_data.csv'):
    return weather.to_csv(f_name, index=False)


# %%

weather = pd.DataFrame()

for loc in locations:
    new_data = clear_df(loc, key, date)
    weather = pd.concat([weather, new_data], ignore_index=True)

# %%
df_csv(weather, "test1.csv")