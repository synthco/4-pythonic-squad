import requests
from bs4 import BeautifulSoup
import datetime as dt
import re

class ISWRequester:
    def __init__(self, url: str):
        self.url = url
        self.soup = self.get_soup()  # main_html
        self.title = self.get_title()  # title
        self.date = self.get_date()  # date
        self.html_data = self._html_raw_parse()  # main_html_v2
        self._raw_data = self._parse_raw()
        self._data_collection = self.to_dict()  # main_text -> to dict


    def get_html_data(self):
        return self.html_data

    @property
    def data_collection(self):
        return self._data_collection

    @property
    def raw_data(self):
        return self._raw_data

    @raw_data.setter
    def raw_data(self, data):
        self._raw_data = data

    @data_collection.setter
    def data_collection(self, data):
        self._data_collection = data

    def get_soup(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        return soup

    def _parse_raw(self):
        field_items_divs = self.soup.find_all("div", class_="field-items")
        res = []
        if field_items_divs and len(field_items_divs) > 1:
            paragraphs = field_items_divs[2].find_all("p") + field_items_divs[2].find_all("ul")
            for paragraph in paragraphs:
                res.append(paragraph.text.strip())
            return res
        else:
            return None

    def _html_raw_parse(self):
        field_items_divs = self.soup.find_all("div", class_="field-items")
        if field_items_divs and len(field_items_divs) > 1:
            paragraphs = field_items_divs[2].find_all("p")
            res = []
            for paragraph in paragraphs:
                res.append(paragraph)
            return res
        else:
            return None

    def raw_out(self):
        for i in self.raw_data:
            print(i)

    def beautify(self):
        self.remove_links()
        # Remove all unnecessary information
        self.raw_data = [data for data in self.raw_data
                         if not data.startswith("Note") and not data.startswith("Click") and data != '']

        for i, row in enumerate(self.raw_data):
            self.raw_data[i] = re.sub(r'\[\d+\]', '', row)

    def remove_links(self):
        # Remove all links at the bottom of the reqest
        links = [link.get('href') for link in self.soup.find_all('a') if link.get('href') is not None]
        self.raw_data = [data for data in self.raw_data if not any(link in data for link in links)]

    def get_date(self):
        if ", " in self.title:
            date_string = self.title.split(", ", 1)[1]
            if "2023" in date_string:
                return dt.datetime.strptime(date_string, "%B %d, %Y").date()
            date = date_string + ", 2022"
            return dt.datetime.strptime(date, "%B %d, %Y").date()
        return None

    def get_title(self):
        # Get title from HTML
        title = self.soup.find("h1")
        return title.text.strip()

    def to_dict(self):
        dict = {}

        dict["date"] = self.date
        dict["title"] = self.title
        dict["full_url"] = self.url
        dict["main_html"] = self.soup
        dict["main_html_v2"] = self.html_data
        dict["main_text"] = self._raw_data

        return dict


if __name__ == "__main__":
    url = "https://understandingwar.org/backgrounder/russian-offensive-campaign-assessment-december-13"
    isw = ISWRequester(url)
    isw.beautify()
    #isw.raw_out()
    new_dict = isw.to_dict()
    #a = new_dict['main_text']
    # for i in a:
    #     print(i)
    #print(new_dict.keys())
