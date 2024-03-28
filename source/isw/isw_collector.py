from isw_requester import ISWRequester
import datetime as dt
import csv
import pandas as pd


class ISWCollector:
    def __init__(self):
        self.urls = []

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
                res_url = base_url + "-" + date.strftime("%B") + "-" + str(date.day)
                url_list.append(res_url)
            else:
                res_url = base_url + "-" + date.strftime("%B") + "-" + str(date.day) + "-" + str(date.year)
                url_list.append(res_url)

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
    def generate_url_yesterday():
        base_url = "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment"
        yesterday = dt.date.today() - dt.timedelta(days=1)
        url = base_url + "-" + yesterday.strftime('%B-%#d-%Y').lower()
        return [url]

    @staticmethod
    def reformat_date(input_date):
        formatted_date = input_date.strftime('%B-%d-%Y').lower()
        return formatted_date

    @staticmethod
    def date_range(start_date, end_date):
        for ordinal in range(start_date.toordinal(), end_date.toordinal()):
            yield dt.date.fromordinal(ordinal)




