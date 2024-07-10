import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def save_to_csv(data, filename='europe_news.csv'):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save")

# URL of the BBC Europe news page
URL = "https://www.bbc.com/news/world/europe"

# Send a GET request to the webpage
response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# List to hold data for each article
data = []

# Find all articles on the page
articles = soup.find_all('div', class_='sc-b8778340-0 kFuHJG')
print(len(articles))  
if not articles:
    print("No articles found")
else:
    for article in articles:
        try:
            # Extract the title
            title_tag = article.find('h2',class_='sc-4fedabc7-3 zTZri')
            title = title_tag.text.strip() if title_tag else 'No title available'
            print(f"Title: {title}")  # Debug print

            # Extract the summary
            summary_tag = article.find('p',class_='sc-b8778340-4 kYtujW')
            summary = summary_tag.text.strip() if summary_tag else 'No summary available'
            print(f"Summary: {summary}")  # Debug print

            # Extract the category
            category_tag = article.find('div', class_='sc-4e537b1-2 eRsxHt')
            category = category_tag.text.strip() if category_tag else 'No category available'
            print(f"Category: {category}")  # Debug print

            # Extract the publication date
            date_tag = article.find('div', class_='sc-4e537b1-1 dsUUMv')
            date = date_tag['datetime'] if date_tag else datetime.now().strftime('%Y-%m-%d')
            print(f"Date: {date}")  # Debug print

            # Append the data to the list
            data.append({
                'Date': date,
                'Title': title,
                'Summary': summary,
                'Category': category
            })
        except Exception as e:
            print(f"Error processing article: {e}")

# Save the data to a CSV file
save_to_csv(data)
