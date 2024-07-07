import pandas as pd
from bs4 import BeautifulSoup
import requests

def scrape_ndtv_africa_news(country_code, pages=3):
    base_url = f"https://www.ndtv.com/world/{country_code}/page-"

    news_title = []
    news_date = []
    news_location = []
    news_url = []

    try:
        for i in range(1, pages + 1):
            url = base_url + str(i)
            news_world = requests.get(url)
            soup = BeautifulSoup(news_world.content, 'html.parser')
            print(f"Scraping page {i} for {country_code.upper()}...")

            # Find the section containing news items
            news_data = soup.find("div", class_="listingNews")

            if news_data:
                # Find all news items
                news_aust = news_data.find_all("div", class_="news_Itm")

                # Extract data for each news item
                for latest in news_aust:
                    try:
                        updated = latest.find("div", class_="news_Itm-cont")
                        date_time = updated.find("span").text.split("|")[1]
                        date = date_time.split(",")
                        try:
                            tit = updated.find("h2", class_="newsHdng")
                            news_title.append(tit.text.strip())
                        except:
                            news_title.append("")
                        try:
                            news_date.append(date[0].strip())
                        except:
                            news_date.append("")
                        try:
                            news_location.append(date[2].strip())
                        except:
                            news_location.append("")
                        try:
                            link = updated.find("a")["href"]
                            news_url.append(link)
                        except:
                            news_url.append("")
                    except Exception as e:
                        print(f"Error in processing news item: {e}")
            else:
                print(f"No news data found on page {i} for {country_code.upper()}")

    except requests.RequestException as e:
        print(f"Error fetching page: {e}")

    # a dictionary for pandas DataFrame
    dic = {
        "title": news_title,
        "date": news_date,
        "location": news_location,
        "url": news_url
    }

    #  a DataFrame
    df = pd.DataFrame(dic)

    # Save DataFrame to CSV file
    filename = f"news_{country_code}_africa.csv"
    df.to_csv(filename, index=False)

    print(f"Data saved to '{filename}'")


countries = ["south-africa", "nigeria", "kenya"]  
for country in countries:
    scrape_ndtv_africa_news(country, pages=3)
