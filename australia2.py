import requests
import pandas as pd
from bs4 import BeautifulSoup
import pycountry
import datetime

url ="https://www.news.com.au/national/breaking-news/page/3"

loca=[]
date=[]
title=[]
category=[]

def HTML():
    code=requests.get(url).content
    soup=BeautifulSoup(code,"lxml")
    newfind=soup.find("div",class_="list l1-s")
    data=newfind.find_all("article",class_="storyblock")
    for dat in data:
        try:
            title.append(dat.find("h4",class_="storyblock_title").text)
        except:
            title.append("")
        try:
            category.append(dat.find("span",class_="storyblock_meta").text)
        except:
            category.append("")
        get_countries(dat.find("p",class_="storyblock_standfirst g_font-body-s"))
        try:
            date.append(datetime.datetime.now().date())
        except:
            date.append("")
    dic={
        "title":title,
        "category":category,
        "date":date,
        "location":loca
    }
    new_csv(dic)


def get_countries(body):
    for x in pycountry.countries:
        if x.name in body:
            loca.append(x.name)
            break
    loca.append("Australia")
    
def new_csv(file):
    df=pd.DataFrame(file)
    df.to_csv("BreakingNews.csv")

HTML()