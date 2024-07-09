import pandas as pd
from bs4 import BeautifulSoup
import requests

url_base = "https://www.ndtv.com/world/asia/page-"
news_title = []
news_date = []
news_location = []
news_url = []

# Adjust the range as per the number of pages you want to scrape
for page_num in range(1, 15):  # Scraping pages 1 to 50
    url = url_base + str(page_num)
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        news_items = soup.find_all("div", class_="news_Itm")
        
        for item in news_items:
            try:
                news_title.append(item.find("h2", class_="newsHdng").text.strip())
            except AttributeError:
                news_title.append("")
            
            try:
                # Extract and split date and location information
                date_location = item.find("div", class_="news_Itm-cont").find("span").text.strip()
                
                # Check if the date_location contains '|'
                if '|' in date_location:
                    date_location_parts = date_location.split("|")[1].split(",")
                    if len(date_location_parts) >= 2:
                        date = date_location_parts[0].strip()
                        location = date_location_parts[1].strip()
                    else:
                        date = ""
                        location = ""
                else:
                    date = ""
                    location = ""
                
                news_date.append(date)
                news_location.append(location)
            except AttributeError:
                news_date.append("")
                news_location.append("")
            
            try:
                news_url.append(item.find("h2", class_="newsHdng").find("a")['href'])
            except AttributeError:
                news_url.append("")
    else:
        print(f"Failed to retrieve page {url}")

# Create a dictionary for DataFrame
news_dict = {
    "Title": news_title,
    "Date": news_date,
    "Location": news_location,
    "URL": news_url
}

# Create DataFrame
df = pd.DataFrame(news_dict)

# Save to CSV with headers and in table form
df.to_csv("news_asia.csv", index=False, encoding='utf-8-sig')

print("Scraping and saving complete!")
