import pandas as pd
from bs4 import BeautifulSoup
import requests

url="https://www.ndtv.com/world/australia/page-"
news_title=[]
news_date=[]
news_location=[]
news_url=[]

for i in range(1,4):
    news_world=requests.get(url+str(i),'lxml')
    soup=BeautifulSoup(news_world.text)
    # print(soup.find("body"))
    print(f"page no.{i}")
    news_data=soup.find("div",class_="lisingNews")
    news_aust=news_data.find_all("div",class_="news_Itm")
    for latest in news_aust:
        try:
            updated=latest.find("div",class_="news_Itm-cont")
            date_time=updated.find("span").text.split("|")[1]
            date=date_time.split(",")
            try:
                tit=updated.find("h2",class_="newsHdng")
                news_title.append(tit.text)
            except:
                news_title.append("")
            try:
                news_date.append(date[0])
            except:
                news_date.append(" ")
            try:
                news_location.append(date[2])
            except:
                news_location.append(" ")
            try:
                link=tit.find("a")
                news_url.append(link)
            except:
                news_url.append(" ")
        except:
            pass

dic={
    "urls":news_url,
    "date":news_date,
    "location":news_location,
    "title":news_title
}

df=pd.DataFrame(dic)
df.to_csv("news_australia.csv")
