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
cat=[]
wars=["ceasefire","dispute","strike","soldier","battlefield"]
pols=["election","PM"]
crimes=["killed","murdered","shotted","theft","robbery","brutal","assault","assaulted"]
sports=["football","runs",'cricket','goals','basketball','hockey','golf','wicket','winner','volleyball']

# Send a GET request to the webpage
for i in range(1,12):
    response = requests.get(f"https://web-cdn.api.bbci.co.uk/xd/content-collection/e2cc1064-8367-4b1e-9fb7-aed170edc48f?country=in&page={i}&size=9")
    response=response.json()
    # print(response['data'][0])
    for dat in response["data"]:
        cate="General"
        title.append(dat['title'])
        date.append(dat['firstPublishedAt'].split('(')[0].split(' G')[0])
        url.append("https://www.bbc.com/"+dat['path'])
        for sport in sports:
            if sport in dat['summary'] or sport in dat['title']:
                cate="sports"
        for crime in crimes:
            if crime in dat['summary'] or crime in dat['title']:
                cate="Crime"
        for pol in pols:
            if pol in dat['summary'] or pol in dat['title']:
                cate="Politics"
        for war in wars:
            if war in dat['summary'] or war in dat['title']:
                cate="War"
        cat.append(cate)
save_to_csv(
    {
        "Title":title,
        "Date":date,
        "URL":url,
        "category":cat       
    }
)