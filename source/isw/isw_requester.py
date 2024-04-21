import requests
from bs4 import BeautifulSoup
import datetime as dt
import pandas as pd
import re
import spacy
import subprocess
import sys
import pickle
import ast
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


class ISWRequester:

    def __init__(self, url=None, date=None):
        if url is None:
            self.url = self.gen_url_yesterday()
        else:
            self.url = url

        self.soup = self.get_soup()  # main_html
        self.title = self.get_title()  # title
        self.date = self.get_date()  # date
        self.html_data = self._html_raw_parse()  # main_html_v2
        self.raw_data = self._parse_raw()

        self.beautify()
        self._data_collection = self.to_dict()  # main_text -> to dict
        # self.pure_text = self.pure()

        self.df = self.to_df()
        self._vector = self.to_vect()

    @property
    def data_collection(self):
        return self._data_collection

    @property
    def data_vect(self):
        return self._vector



    @staticmethod
    def gen_url_yesterday() -> str:
        base_url = "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment"
        yesterday = dt.date.today() - dt.timedelta(days=1)
        url = base_url + "-" + yesterday.strftime('%B-%d-%Y').lower()
        print(url)
        return url

    def get_soup(self) -> BeautifulSoup:
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        return soup

    def _parse_raw(self):
        field_items_divs = self.soup.find_all("div", class_="field-items")
        if field_items_divs and len(field_items_divs) > 1:
            paragraphs = field_items_divs[2].find_all("p") + field_items_divs[2].find_all("ul")
            res = []
            for paragraph in paragraphs:
                res.append(paragraph.text.strip())
            if len(res) == 0:
                paragraphs = field_items_divs[1].find_all("p")
                for paragraph in paragraphs:
                    res.append(paragraph.text.strip())
            return res
        return None

    def _html_raw_parse(self):
        field_items_divs = self.soup.find_all("div", class_="field-items")
        if field_items_divs and len(field_items_divs) > 1:
            paragraphs = field_items_divs[2].find_all("p")
            res = []
            for paragraph in paragraphs:
                res.append(paragraph)
            if len(res) == 0:
                paragraphs = field_items_divs[1].find_all("p")
                for paragraph in paragraphs:
                    res.append(paragraph)
            return res
        return None

    def raw_out(self):
        for i in self.raw_data:
            print(i)

    def beautify(self):
        if self.raw_data is not None:
            self.raw_data.pop(0)
            self.raw_data.pop(0)
            self.remove_links()
            # Remove all unnecessary information
            self.raw_data = [data for data in self.raw_data
                             if not data.startswith("Note") and not data.startswith("Click") and data != '']

            for i in range(len(self.raw_data)):
                # delete [1], [2], [3]...
                self.raw_data[i] = re.sub(r'\[\d+\]', '', self.raw_data[i])
                # delete \xa0
                self.raw_data[i] = re.sub(r'\xa0', '', self.raw_data[i])
                self.raw_data[i] = re.sub(r'\n', '', self.raw_data[i])

    def remove_links(self):
        # Remove all links at the bottom of the request
        links = [link.get('href') for link in self.soup.find_all('a') if link.get('href') is not None]
        self.raw_data = [data for data in self.raw_data if not any(link in data for link in links)]

    def get_date(self):
        if ", " in self.title:
            date_string = self.title.split(", ", 1)[1]
            if "2023" in date_string:
                return dt.datetime.strptime(date_string, "%B %d, %Y").date()
            elif "2022" in date_string:
                return dt.datetime.strptime(date_string, "%B %d, %Y").date()
            elif "2024" in date_string:
                return dt.datetime.strptime(date_string, "%B %d, %Y").date()
            date = date_string + ", 2022"
            return dt.datetime.strptime(date, "%B %d, %Y").date()
        return None

    def get_title(self):
        # Get title from HTML
        title = self.soup.find("h1")
        return title.text.strip()

    # convertation to dict
    def to_dict(self) -> dict:
        res = {"date": self.date, "title": self.title, "full_url": self.url, "main_html": self.soup,
               "main_html_v2": self.html_data, "main_text": self.raw_data}
        return res

    # convertation to DataFrame
    def to_df(self):
        df = pd.DataFrame({"date": [self.data_collection["date"]], "main_text": [self.data_collection["main_text"]]})
        return df

    # method for vectorization
    def to_vect(self):
        # TODO add if module is not downoladed -> download
        if not spacy.util.is_package("en_core_web_sm"):
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

        nlp = spacy.load("en_core_web_sm")


        # lemmatizing
        def lemmatize_text(text):
            doc = nlp(text)
            lemmatized_text = ' '.join([token.lemma_ for token in doc])
            return lemmatized_text



        # lowercasing
        def lowercase_text(text):
            # sample = ast.literal_eval(text)
            return [i.lower() for i in text]

        # text cleaning from odd elements
        def clean_text(text_list):
            # Ensure input is a list of strings
            if not all(isinstance(text, str) for text in text_list):
                raise ValueError("Input must be a list of strings")

            cleaned_text = ' '.join(text_list)

            # Perform text cleaning operations
            cleaned_text = re.sub(
                r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b',
                lambda match: match.group(0).lower(), cleaned_text, flags=re.IGNORECASE)

            cleaned_text = re.sub(r'[-/\\—\xa0"’“]', ' ', cleaned_text)
            cleaned_text = re.sub(r'[’“]', ' ', cleaned_text)
            cleaned_text = re.sub(r'(march)', ' ', cleaned_text)
            cleaned_text = re.sub(r'\n', ' ', cleaned_text)
            cleaned_text = re.sub(r'\b(?:pm|am)\b', '', cleaned_text)
            cleaned_text = re.sub(r'\b(?:\d+(?:st|nd|rd|th)?)\b', '', cleaned_text)
            cleaned_text = re.sub(r'\b\d+[a-zA-Z]+|(?<!\d)[a-zA-Z]+\d+\b', '', cleaned_text)
            cleaned_text = re.sub(r'\b\w\b', '', cleaned_text)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text.strip())

            return cleaned_text

        # stopword removal
        def remove_stopwords(text):
            ", ".join(stopwords.words('english'))
            STOPWORDS = set(stopwords.words('english'))
            return " ".join([word for word in str(text).split() if word not in STOPWORDS])

        pure = self.df

        # use lowercasing
        pure["main_text"] = pure["main_text"].apply(lowercase_text)

        # clean text
        pure['new'] = pure['main_text'].apply(lambda x: clean_text(x))
        pure["main_text"] = pure["new"]
        pure.drop(["new"], axis=1)

        # remove stopwords
        pure["text_wo_stop"] = pure["main_text"].apply(lambda text: remove_stopwords(text))

        # lemmatizing
        pure['text_for_vect2'] = pure['text_wo_stop'].apply(lemmatize_text)

        # dropping out all useless columns
        pure.drop(["text_wo_stop", "main_text"], axis=1)

        # vectorizing
        #ENTER THE RIGHT PATH

        with open("/Users/ivantyshchenko/Documents/GitHub/4-pythonic-squad/source/isw/tfidf_vect.pkl", "rb") as f:
            tfidf_vect = pickle.load(f)

        tfidf_matrix = tfidf_vect.transform(pure['text_for_vect2'])
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vect.get_feature_names_out())
        new_column_names = ['isw_{}'.format(i + 1) for i in range(len(tfidf_df.columns))]
        tfidf_df.columns = new_column_names
        vect_df = pd.concat([pure["date"], tfidf_df], axis=1)

        return vect_df


if __name__ == "__main__":
    requster = ISWRequester()
    print(requster._vector)
