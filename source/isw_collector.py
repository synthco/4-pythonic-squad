from isw_requester import ISWRequester
import csv
import pandas as pd
import datetime as dt
class ISWCollector:
    def __init__(self):
        self.urls = []
        self.data = pd.DataFrame(
            columns=["url", "title", "date", "html_text", "text"])

    @staticmethod
    def collect(url):
        req = ISWRequester(url)
        json_data = req.to_dict()
        return json_data

    def add_url(self, url: list):
        for link in url:
            if link not in self.urls:
                self.urls.append(link)

    def add_url(self, url: str):
        if url not in self.urls:
            self.urls.append(url)

    @staticmethod
    def generate_url_roca():
        base_url = "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment"
        date_range_generator = ISWCollector.date_range(dt.date(2022, 2, 24), dt.date(2023, 1, 25))
        url_list = []
        for date in date_range_generator:
            if date.year == 2022:
                url_list.append(base_url + "-" + date.strftime("%B-%d"))
            else:
                url_list.append(base_url + "-" + ISWCollector.reformat_date(date))
        return url_list

    @staticmethod
    def reformat_date(input_date):
        formatted_date = input_date.strftime('%B-%d-%Y').lower()
        return formatted_date

    @staticmethod
    def date_range(start_date, end_date):
        for ordinal in range(start_date.toordinal(), end_date.toordinal()):
            yield dt.date.fromordinal(ordinal)


if __name__ == "__main__":
    isw_collector = ISWCollector()
    isw_collector.add_url(isw_collector.generate_url_roca())
    #print(isw_collector.urls)

    instances = []

    for i in range(len(isw_collector.urls[0])):
        url = isw_collector.urls[0][i]
        # response = requests.get(url)
        # if response.status_code != 404:
        instances.append(ISWRequester(url))

    with open("ISW.csv", "w", newline="", encoding='utf-8') as csvfile:
        a = instances[0]
        data_dict = a.to_dict()
        fieldnames = list(data_dict.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for instance in instances:
            instance.beautify()
            data_dict = instance.to_dict()
            writer.writerow(data_dict)
