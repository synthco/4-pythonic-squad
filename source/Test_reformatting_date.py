import datetime as dt


def reformat_date(input_date):
    formatted_date = input_date.strftime('%B-%d-%Y').lower()
    return formatted_date


def date_range(start_date, end_date):
    for ordinal in range(start_date.toordinal(), end_date.toordinal()):
        yield dt.date.fromordinal(ordinal)


def generate_url_2022():
    base_url = "https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment"
    date_range_generator = date_range(dt.date(2023, 2, 23), dt.date(2023, 2, 27))
    url_list = []
    for date in date_range_generator:
        url_list.append(base_url + "-" + reformat_date(date))

    for url in url_list:
        print(url)


generate_url_2022()
