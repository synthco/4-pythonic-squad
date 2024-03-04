from isw_requester import ISWRequester
# import csv
import pandas as pd
import datetime as dt
class ISWCollector:
    def __init__(self):
        self.urls  = []
        self.data = pd.DataFrame(
            columns=["url", "title", "date", "html_text", "text"])

    @staticmethod
    def collect(url):
        req = ISWRequester(url)
        json_data = req.to_json()
        return json_data

    def add_url(self, url: list):
        for link in url:
            if link not in self.urls:
                self.urls.append(link)

    def add_url(self, url: str):
        if url not in self.urls:
            self.urls.append(url)

    @staticmethod
    def date_range(start_date, end_date):
        for ordinal in range(start_date.toordinal(), end_date.toordinal()):
            yield dt.date.fromordinal(ordinal)


    @staticmethod
    def generate_url_2022():
        base_url = "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment"
        start_date = dt.date(2022, 2, 24)
        end_date = dt.date(2023, 1, 1)
        date_range = ISWCollector.date_range(start_date, end_date)
        url_list = []

        for date in date_range:
            formatted_date = date.strftime("%B-%#d").lower()
            url_list.append(base_url + "-" + formatted_date)
        return url_list


# https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-26-2024
if __name__ == "__main__":
    url = "https://understandingwar.org/backgrounder/russian-offensive-campaign-assessment"
    isw_collection = ISWCollector()
    urls = isw_collection.generate_url_2022()
    print(urls)

