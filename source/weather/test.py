from weather_collector import WeatherCollector
from datetime import datetime

current_date = datetime.now()
collector = WeatherCollector(current_date)
weather_data = collector.data
#test csv
collector.weather_data.to_csv("wtest.csv", index=False)

print(weather_data)
print(collector.weather_data)
