from source.isw.isw_requester import ISWRequester
from datetime import datetime


class Dfender:
    """
    Date in format YYYY-MM-DD or in Datetime object
   """

    def __init__(self, date=None):

        # Date processing
        if date is None:
            self.__date = datetime.now()
        elif type(date) is not datetime:
            try:
                self.__date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError as e:
                print(f"Date format not valid: {e}")
                print("Date in format YYYY-MM-DD or in Datetime object")

        self.__isw = self.request_isw()
        self.__isw_vector = self.isw_vectorize()

        # self.__weather = self.request_weather()

        # self.__vector = self.full_merge()

        self.__result = None

    @property
    def date(self):
        return self.__date

    @property
    def isw(self):
        return self.__isw

    @property
    def isw_vector(self):
        return self.__isw_vector

    @property
    def weather(self):
        return self.__weather

    def __repr__(self):
        res = {
            "date": self.date

        }
        return str(res)

    def request_isw(self):
        reqester = ISWRequester()
        return reqester.data_collection



# https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-april-9-2024
# https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-april-09-2024