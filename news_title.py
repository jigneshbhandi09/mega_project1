import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
# Function to scrape news data
def scrape_south_america_news():
    url = 'https://apnews.com/hub/south-america'  

    # Send a GET request to the URL
    country="south-america"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        news_articles = []

        articles = soup.findAll('div', class_='PagePromo-content')

        for article in articles:
            next_part= article.find('a', class_='Link')
            page_url= next_part.get('href')
            title= next_part.find('span',class_='PagePromoContentIcons-text').text

            timestamp_element = article.find('bsp-timestamp')
            if timestamp_element:
                timestamp = timestamp_element.get('data-timestamp')
                # Convert timestamp to datetime object
                date = datetime.utcfromtimestamp(int(timestamp) / 1000).strftime('%Y-%m-%d')
            response = requests.get(page_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                try:
                    categories=soup.find('div',class_='Page-breadcrumbs').text
                except:
                    categories="other"
                    
                news_articles.append({
                    'date': date,
                    'title': title,
                    'country':country,
                    'categories': categories,
                    'source_link': page_url,
                })

        return news_articles
    else:
        print(f"Failed to retrieve page: {response.status_code}")

# Function to write data to CSV file
def write_to_csv(news_articles, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['date', 'location', 'title', 'categories', 'source_link']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for article in news_articles:
            writer.writerow(article)


south_america_news = scrape_south_america_news()
write_to_csv(south_america_news, 'south_america.csv')
