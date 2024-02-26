import requests
import json
from bs4 import BeautifulSoup

url = "https://www.understandingwar.org/backgrounder/ukraine-conflict-updates-2022"
r = requests.get(url)
print(r.status_code)
soup = BeautifulSoup(r.text, "html.parser")
dates  = soup.select("#block-system-main div.field.field-name-body.field-type-text-with-summary.field-label-hidden div div div:nth-child(1)")

print(dates)
date_element = soup.select_one("#block-system-main > div > div > div.field.field-name-body.field-type-text-with-summary.field-label-hidden > div > div > div:nth-child(1) > p:nth-child(15) > strong")
print (date_element)




#block-system-main > div > div > div.field.field-name-body.field-type-text-with-summary.field-label-hidden > div > div > div:nth-child(1) > p:nth-child(15) > strong
#block-system-main > div > div > div.field.field-name-body.field-type-text-with-summary.field-label-hidden > div > div > div:nth-child(1) > p:nth-child(31) > strong