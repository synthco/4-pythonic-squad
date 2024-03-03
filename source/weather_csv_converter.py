import requests
import pandas as pd
import csv
from datetime import datetime, timedelta

#initializing current date and next date
# initializing current time as well
current_date = datetime.now()
one_day_delta = timedelta(days=1)
next_day = current_date + one_day_delta
date1 = current_date.strftime("%Y-%m-%d")
date2 = next_day.strftime("%Y-%m-%d")
time = current_date.strftime("%H-00-00")

#creating the list of all counties, adding api-key
# API - https://www.visualcrossing.com
#your API-key here:
key = ""
locations = ["Kyiv", "Rivne", "Lutsk", "Lviv", "Zhytomyr",
             "Chernivtsi", "Ivano-Frankivsk", "Ternopil", "Khmelnytskyi",
             "Uzhhorod", "Vinnytsia", "Cherkasy", "Poltava", "Chernihiv",
             "Sumy", "Kharkiv", "Kropyvnytskyi", "Dnipro", "Mykolaiv",
             "Kharkiv", "Luhansk", "Donetsk", "Odesa", "Chernihiv",
             "Kherson"]


#function to make csv from json response
def json_to_csv(key, location, date1, date2, output_file="test1.csv"):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location},Ukraine/{date1}/{date2}?key={key}"

    #getting response and converting into json
    response = requests.get(url)
    data = response.json()

    #collecting all attributes from json as keys from dict
    if 'days' in data:
        with open(output_file, "w", newline="", encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            #most info is located in "days" and we also have hourly data for each day
            # but don't forget about general info!(others)
            others = {key: data[key] for key in
                      ['latitude', 'longitude', 'resolvedAddress', 'address', 'timezone', 'tzoffset']}
            daily_data = data['days']
            hourly_keys = set()

            for day_data in daily_data:
                hourly_data = day_data.get('hours', [])
                for hour_data in hourly_data:
                    hourly_keys.update(hour_data.keys())

            all_keys = list(others.keys()) + list(daily_data[0].keys()) + list(hourly_keys)
            writer.writerow(all_keys)
            #getting values for all keys via iteration through all dict and writing it to the csv file
            for day in daily_data:
                day_values = [day.get(key, "") for key in daily_data[0].keys()]
                for hour in day["hours"]:
                    hourly_values = [hour.get(key, "") for key in hourly_keys]
                    row = [others.get(key, "") for key in others.keys()] + day_values + hourly_values
                    writer.writerow(row)

        print(f"Data has been written to {output_file}")
    #returning the name of csv file
    return output_file

#function for finding time point in dataset which is equal to current time
def find_datetime(time):
    current = int(time.split("-")[0])  # Splitting the time string and accessing the hour part
    for hour in range(24):
        if hour == current:
            return hour
    return 0

def to_celsius(x):
    return (x - 32) * (5 / 9)

#creating a clear df from api-resppnse (easiest way to work with data)
def clear_df(location, key, date1, date2):
    data = json_to_csv(key, location, date1, date2)
    df = pd.read_csv(data)
    #dropping an extra column which was duplicated in "keys" in previous function
    #because of the specific of json
    df.drop(["hours"], axis=1, inplace=True)
    #converting values of temp
    columns_to_convert = ['tempmax', 'temp', 'tempmin', 'feelslike', 'feelslikemax', 'feelslikemin']
    df[columns_to_convert] = (df[columns_to_convert] - 32) * (5 / 9)
    #changing names for hourly columns
    for col in df.columns:
        if ".1" in col:
            new_col_name = col.replace(".1", "_hourly")
            df.rename(columns={col: new_col_name}, inplace=True)

    df=df.fillna(0)
    #using function to cut 12-hour-period in dataframe we're interested in
    cut = find_datetime(time)
    df = df.iloc[cut:cut+12]

    #dropping several columns
    columns_to_add = ["sunsetEpoch_hourly", "moonphase_hourly", "sunrise_hourly", "sunset_hourly", "sunriseEpoch_hourly"]

    for col in columns_to_add:
        df[col] = 0
    df = df.drop(columns_to_add, axis=1)
    #yay! finally
    return df

#converts to csv. it's not neccesarily to put it in function tho
def df_csv(df, f_name='weather_data.csv'):
    return df.to_csv(f_name, index=False)  # Corrected variable name to 'df'

def main():
    weather = pd.DataFrame()

    for loc in locations:
        new_data = clear_df(loc, key, date1, date2)
        weather = pd.concat([weather, new_data], ignore_index=True)

    df_csv(weather, "test1.csv")


main()

#check test file here:
# pd.read_csv("test1.csv")
