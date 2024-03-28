import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def isNaN(num):
    return num != num


df_events = pd.read_csv('alarms.csv', sep=';')
df_events_v2 = df_events.drop(["id", "region_id"], axis=1)

df_events_v2["start_time"] = pd.to_datetime(df_events_v2["start"])
df_events_v2["end_time"] = pd.to_datetime(df_events_v2["end"])
# df_events_v2["event_time"] = pd.to_datetime(df_events_v2["event_time"])

df_events_v2["start_hour"] = df_events_v2['start_time'].dt.floor('h')
df_events_v2["end_hour"] = df_events_v2['end_time'].dt.ceil('h')
# df_events_v2["event_hour"] = df_events_v2['event_time'].dt.round('H')

df_events_v2["start_hour"] = df_events_v2.apply(lambda x: x["start_hour"] if not isNaN(x["start_hour"]) else x["event_hour"] , axis=1)
df_events_v2["end_hour"] = df_events_v2.apply(lambda x: x["end_hour"] if not isNaN(x["end_hour"]) else x["event_hour"] , axis=1)

df_events_v2["day_date"] = df_events_v2["start_time"].dt.date

df_events_v2["start_hour_datetimeEpoch"] = df_events_v2['start_hour'].apply(lambda x: int(x.strftime('%s'))  if not isNaN(x) else None)
df_events_v2["end_hour_datetimeEpoch"] = df_events_v2['end_hour'].apply(lambda x: int(x.strftime('%s'))  if not isNaN(x) else None)

print(df_events_v2.head(10))

df_weather = pd.read_csv('all_weather_by_hour_v2.csv')
df_weather["day_datetime"] = pd.to_datetime(df_weather["day_datetime"])
print(df_weather.shape)
print(df_weather.head(5))

weather_exclude = [
"day_feelslikemax",
"day_feelslikemin",
"day_sunriseEpoch",
"day_sunsetEpoch",
"day_description",
"city_latitude",
"city_longitude",
"city_address",
"city_timezone",
"city_tzoffset",
"day_feelslike",
"day_precipprob",
"day_snow",
"day_snowdepth",
"day_windgust",
"day_windspeed",
"day_winddir",
"day_pressure",
"day_cloudcover",
"day_visibility",
"day_severerisk",
"day_conditions",
"day_icon",
"day_source",
"day_preciptype",
"day_stations",
"hour_icon",
"hour_source",
"hour_stations",
"hour_feelslike"
]

df_weather_v2 = df_weather.drop(weather_exclude, axis=1)

df_weather_v2["city"] = df_weather_v2["city_resolvedAddress"].apply(lambda x: x.split(",")[0])
df_weather_v2["city"] = df_weather_v2["city"].replace('Хмельницька область', "Хмельницький")

print(df_weather_v2.head(5))

print(df_weather_v2.shape)

df_regions = pd.read_csv('regions.csv')

df_weather_reg = pd.merge(df_weather_v2, df_regions, left_on="city", right_on="center_city_ua")

print(df_weather_reg.head(10))

print(df_events_v2.dtypes)

print(df_events_v2.shape)

events_dict = df_events_v2.to_dict('records')
events_by_hour = []

print(events_dict[0])

for event in events_dict:
    for d in pd.date_range(start=event["start_hour"], end=event["end_hour"], freq='1H'):
        et = event.copy()
        et["hour_level_event_time"] = d
        events_by_hour.append(et)

df_events_v3 = pd.DataFrame.from_dict(events_by_hour)
print(df_events_v3["hour_level_event_time"])
df_events_v3["hour_level_event_datetimeEpoch"] = df_events_v3["hour_level_event_time"].apply(lambda x: int(x.strftime('%s'))  if not isNaN(x) else None)
df_events_v4 = df_events_v3.copy().add_prefix('event_')

print(df_events_v4.head(5))
df_weather_v4 = df_weather_reg.merge(df_events_v4,
                                     how="left",
                                     left_on=["region_alt", "hour_datetimeEpoch"],
                                     right_on=["event_region_title", "event_hour_level_event_datetimeEpoch"])

print(df_weather_v4.shape)

df_weather_v4.to_csv('weather_v4.csv', sep=";", index=False)




