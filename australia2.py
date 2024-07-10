import requests
import pandas as pd
from bs4 import BeautifulSoup
import pycountry
import datetime

url ="https://www.news.com.au/national/breaking-news/page/"

loca=[]
date=[]
title=[]
url1=[]
category=[]

def HTML(i):
    code=requests.get(url+str(i)).content
    soup=BeautifulSoup(code,"lxml")
    newfind=soup.find("div",class_="list l1-s")
    data=newfind.find_all("article",class_="storyblock")
    for dat in data:
        country="Australia"
        try:
            titles=dat.find("h4",class_="storyblock_title")
            title.append(titles.text)
            
            urls=titles.find('a')
            url1.append(urls.get('href'))
        except:
            title.append("")
            url1.append("")
        try:
            category.append(dat.find("span",class_="storyblock_meta").text)
        except:
            category.append("")
        get_countries(dat.find("p",class_="storyblock_standfirst g_font-body-s"))
        loca.append(country)
        try:
            date.append(datetime.datetime.now().date())
        except:
            date.append("")
    dic={
        "title":title,
        "category":category,
        "date":date,
        "location":loca,
        "url":url1
    }
    new_csv(dic)


def get_countries(body):
    print(len(pycountry.countries))
    for x in pycountry.countries:
        if x.name in body:
            country=x.name
            break
    
def new_csv(file):
    df=pd.DataFrame(file)
    df.to_csv("BreakingNews.csv")

for i in range(1,10):
    HTML(i)