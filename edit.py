import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def save_to_csv(data, filename='Europe_News.csv'):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save")

# URL of the BBC Europe news page
title=[]
date=[]
url=[]

# Send a GET request to the webpage
for i in range(1,10):
    response = requests.get(f"https://web-cdn.api.bbci.co.uk/xd/content-collection/e2cc1064-8367-4b1e-9fb7-aed170edc48f?country=in&page={i}&size=9")
    response=response.json()
    for dat in response["data"]:
          title.append(dat['title'])
    date.append(dat['firstPublishedAt'].split('(')[0].split(' G')[0])
    url.append("https://www.bbc.com/"+dat['path'])

save_to_csv(
    {
        "Title":title,
        "Date":date,
        "URL":url       
    }
)