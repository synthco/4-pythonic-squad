from isw_requester import ISWRequester
from isw_collector import ISWCollector
import csv
import pandas as pd


if __name__ == '__main__':
    isw_collector = ISWCollector()
    isw_collector.add_url(isw_collector.generate_url_roca())

    instances = []

    for i in range(len(isw_collector.urls[0])):
        url = isw_collector.urls[0][i]
        r = ISWRequester(url)
        instances.append(r)
        print(f"url - {url}, status code - {r.title}")

    with open("ISW01.csv", "w", newline="", encoding='utf-8') as csvfile:
        a = instances[0]
        data_dict = a.to_dict()
        fieldnames = list(data_dict.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for instance in instances:
            instance.beautify()
            data_dict = instance.to_dict()
            writer.writerow(data_dict)

    df = pd.read_csv("ISW01.csv")

    # print(df)

    df.dropna(subset=["date"], inplace=True)

    # print(df)

    df.to_csv("ISW01.csv", index=False)

    isw_yesterday = ISWCollector()
    isw_yesterday.add_url(isw_yesterday.generate_url_yesterday())
    a = isw_yesterday.urls[0]
    # print(a)
    isw_req = ISWRequester(a[0])

    isw_req.beautify()
    b = isw_req.to_dict()
    data_dict = isw_req.to_dict()
    df_yesterday = pd.DataFrame(columns=data_dict.keys())
    df_yesterday = pd.concat([df, pd.DataFrame([b])], ignore_index=True)
    # print(df_yesterday)

    df.dropna(subset=["date"], inplace=True)

    # print(df)

    df.to_csv("ISW.csv", index=False)