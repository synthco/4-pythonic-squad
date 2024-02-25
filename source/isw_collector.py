import requests
from bs4 import BeautifulSoup

class ISWCollector:
    def __init__(self, url: str):
        self.url = url
        self._data_collection = []

    def create_soup(self):
        data = requests.get(self.url).text
        soup = BeautifulSoup(data, 'html.parser')
        return soup

    @property
    def data_collection(self):
        return self._data_collection

    @data_collection.setter
    def data_collection(self, data):
        self._data_collection = data

