import requests
from bs4 import BeautifulSoup


class ISWCollector:
    def __init__(self, url: str):
        self.url = url
        self._data_collection = []
        self._raw_data = self._parse_raw()
        self.title = self.get_title()


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

    def _parse_raw(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        field_items_divs = soup.find_all("div", class_="field-items")
        if field_items_divs:
            paragraphs = field_items_divs[2].find_all("p")
            res = []
            for paragraph in paragraphs:
                res.append(paragraph.text.strip())

        else:
            raise Exception("No Paragraphs found")
        return res

    def raw_out(self):
        for i in range(self.raw_data.__len__()):
            print(self.raw_data[i])

    def beautify(self):
        #Remove all unnecessary information
        pass

    def get_date(self):
        #get date and time from html
        pass

    def get_title(self):
        #Get title from HTML
        pass

    def to_json(self):
        #Convert pure data to json
        pass





if __name__ == "__main__":
    url = "https://understandingwar.org/backgrounder/russian-offensive-campaign-assessment-december-3"
    isw = ISWCollector(url)
    isw.raw_out()

