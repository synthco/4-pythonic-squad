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
        date_range_generator = ISWCollector.date_range(dt.date(2022, 3, 1), dt.date(2023, 1, 26))
        # for days from 25.02.2022 to 28.02.2022
        url_list = ["https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-25-2022",
                    "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-26",
                    "https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-27",
                    "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-28-2022"]

        for date in date_range_generator:
            if date.year == 2022:
                url_list.append(base_url + "-" + date.strftime("%B-%#d"))
            else:
                url_list.append(base_url + "-" + ISWCollector.reformat_date(date))

        problem_url = ["https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-May-5",
                       "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-July-11",
                       "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-August-12",
                       "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-November-24",
                       "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-December-25",
                       "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-january-1-2023"]

        for url in url_list:
            if url in problem_url:
                url_list.remove(url)

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

    instances = []

    for i in range(len(isw_collector.urls[0])):
        url = isw_collector.urls[0][i]
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

    df = pd.read_csv("ISW.csv")

    print(df)

    df.dropna(subset=["date"], inplace=True)

    print(df)

    df.to_csv("ISW.csv", index=False)
