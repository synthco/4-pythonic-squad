from isw_requester import ISWRequester
from isw_collector import ISWCollector
import pandas as pd


if __name__ == "__main__":
    isw_collector = ISWCollector()
    isw_collector.generate_url_roca()

    isw_requester = ISWRequester(isw_collector.urls[0])

    df = pd.DataFrame(columns=isw_requester.to_dict().keys())

    for url in isw_collector.urls:
        requester = ISWRequester(url)
        requester.beautify()
        row_dict = requester.to_dict()
        df = df._append(row_dict, ignore_index=True)

    df.dropna(subset=["date"], inplace=True)

    df.to_csv("ISW.csv", index=False)
