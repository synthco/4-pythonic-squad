import requests
from bs4 import BeautifulSoup
import datetime as dt

class ISWRequester:
    def __init__(self, url: str):
        self.url = url
        self.soup = self.get_soup()                       #main_html
        self.title = self.get_title()                           #titile
        self.date = self.get_date()                         #date
        self.html_data = self._html_raw_parse()  #main_html_v2
        self._raw_data = self._parse_raw()
        self._data_collection = None  # main_text -> to dict



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
        if field_items_divs:
            paragraphs = field_items_divs[2].find_all("p")
            res = []
            for paragraph in paragraphs:
                res.append(paragraph.text.strip())

        else:
            raise Exception("No Paragraphs found")
        return res

    def _html_raw_parse(self):
        field_items_divs = self.soup.find_all("div", class_="field-items")
        if field_items_divs:
            paragraphs = field_items_divs[2].find_all("p")
            res = []
            for paragraph in paragraphs:
                res.append(paragraph)
        pass

    def raw_out(self):
        for i in range(self.raw_data.__len__()):
            print(self.raw_data[i])

    def beautify(self):
        self.remove_links()
        #Remove all unnecessary information
        pass


    def remove_links(self):
        #Remove all links at the bottom of the reqest

        pass
    def get_date(self):
        date_string = self.title.split(", ", 1)[1]
        print(date_string)
        if "2023" in date_string:
            return dt.datetime.strptime(date_string, "%B %d, %Y").date()
        else:
            date = date_string + ", 2022"
            return dt.datetime.strptime(date, "%B %d, %Y").date()




    def get_title(self):
        #Get title from HTML
        title = self.soup.find("h1")

        return title.text.strip()


    def to_dict(self):
        #Convert pure data to dict
        #ask Andrew WTF is main_html and main_html_v2?
        # date
        # short_url
        # title
        # text_title
        # full_url
        # main_html
        # main_html_v2
        # main_text
        pass



if __name__ == "__main__":
    url = "https://understandingwar.org/backgrounder/russian-offensive-campaign-assessment-december-12"
    isw = ISWRequester(url)
    # isw.raw_out()
    print (isw.title)
    print(isw.date)
    # print(isw.soup)



