import pandas as pd
import ast
'''
df_weather_event_v1 = pd.read_csv('weather_v4.csv', sep=';')

print(df_weather_event_v1.head(5))


def isNaN(num):
    return num != num


print(isNaN(df_weather_event_v1['event_hour_level_event_datetimeEpoch'][0]))

df_weather_event_v1['is_alarm'] = df_weather_event_v1['event_hour_level_event_datetimeEpoch'].apply(lambda x: 0 if isNaN(x) else 1)

print(df_weather_event_v1.head(70))

df_weather_event_v1.to_csv('weather_v5.csv', sep=';')



df_all_data = pd.read_csv('weather_v5.csv', sep=';')

df_isw_data = pd.read_csv('vectorised_texts.csv')

print(df_all_data.dtypes)

data_exclude = ['city_resolvedAddress',
                'day_datetimeEpoch',
                'day_sunrise', 'day_sunset',
                'hour_datetime',
                'hour_datetimeEpoch',
                'city',
                'region',
                'center_city_ua',
                'center_city_en',
                'region_alt',
                'event_region_title',
                'event_region_city',
                'event_start',
                'event_end',
                'event_clean_end',
                'event_start_time',
                'event_end_time',
                'event_start_hour',
                'event_end_hour',
                'event_day_date',
                'event_start_hour_datetimeEpoch',
                'event_end_hour_datetimeEpoch',
                'event_hour_level_event_time',
                'event_hour_level_event_datetimeEpoch']


df_weather_event_final = df_all_data.drop(data_exclude, axis=1)
df_weather_event_final = df_weather_event_final.drop('Unnamed: 0', axis=1)
print(df_weather_event_final.head(5))

df_weather_event_final.to_csv('df_weather_event_final.csv', index=False)





def isNaN(num):
    return num != num


df_weather_final = pd.read_csv('df_weather_event_final.csv')

df_weather_final['hour_preciptype'] = df_weather_final['hour_preciptype'].fillna(0)

# print(df_weather_final['hour_preciptype'])

unique_values = df_weather_final['hour_preciptype'].unique()

for value in unique_values:
    print(value)

precip_type_mapping = {
    "['snow']": 1,
    0: 0,
    "['rain']": 2,
    "['rain', 'snow']": 3,
    "['freezingrain']": 4,
    "['ice']": 5
}

df_weather_final['hour_preciptype'] = df_weather_final['hour_preciptype'].replace(precip_type_mapping)

#print(df_weather_final['hour_preciptype'])

df_weather_final['hour_solarradiation'] = df_weather_final['hour_solarradiation'].fillna(-1)
df_weather_final['hour_solarenergy'] = df_weather_final['hour_solarenergy'].fillna(-1)
df_weather_final['hour_uvindex'] = df_weather_final['hour_uvindex'].fillna(-1)
df_weather_final['event_intersection_alarm_id'] = df_weather_final['event_intersection_alarm_id'].fillna(-1)
df_weather_final['event_all_region'] = df_weather_final['event_all_region'].fillna(-1)

unique_values_2 = df_weather_final['hour_conditions'].unique()

for value in unique_values_2:
    print(value)

conditions_mapping = {
    'Overcast': 1,
    'Partially cloudy': 2,
    'Snow, Overcast': 3,
    'Clear': 4,
    'Rain, Overcast': 5,
    'Rain, Partially cloudy': 6,
    'Snow, Rain, Partially cloudy': 7,
    'Snow, Partially cloudy': 8,
    'Snow, Rain, Overcast': 9,
    'Rain': 10,
    'Freezing Drizzle/Freezing Rain, Overcast': 11,
    'Snow': 12,
    'Snow, Rain': 13,
    'Ice, Overcast': 14
}

df_weather_final['hour_conditions'] = df_weather_final['hour_conditions'].replace(conditions_mapping)

df_weather_final.to_csv('df_weather_event_final_v2.csv', index=False)



'''
df_weather_events_final = pd.read_csv('final_weather_alarms.csv')

df_isw_vectorised_data = pd.read_csv('isw_tfidf.csv')

df_weather_events_final = df_weather_events_final.rename(columns={'day_datetime': 'date'})

print(df_weather_events_final.shape)
print(df_isw_vectorised_data.shape)

merged_df = pd.merge(df_weather_events_final, df_isw_vectorised_data, on='date')
print(merged_df.shape)

column_to_move = merged_df.pop('is_alarm')
merged_df['is_alarm'] = column_to_move

# merged_df.to_csv('final_dataset.csv', index=False)

print(merged_df.shape)
print(merged_df)
