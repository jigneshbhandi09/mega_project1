import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the BBC News US & Canada page
url = "https://www.bbc.com/news/us-canada"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all news items
    news_items = soup.find_all("div", {"data-testid": "card-text-wrapper"})
    
    # Initialize lists to store data
    news_data = []

    # Iterate over each news item
    for item in news_items:
        try:
            # Extract title
            title = item.find("h2", {"data-testid": "card-headline"}).get_text().strip()
        except AttributeError:
            title = ""

        try:
            # Extract paragraph
            paragraph = item.find("p", {"data-testid": "card-description"}).get_text().strip()
        except AttributeError:
            paragraph = ""

        try:
            # Extract date and time
            date_time = item.find("span", {"data-testid": "card-metadata-lastupdated"}).get_text().strip()
        except AttributeError:
            date_time = ""

        try:
            # Extract location
            location = item.find("span", {"data-testid": "card-metadata-tag"}).get_text().strip()
        except AttributeError:
            location = ""

        # Append data to list as a dictionary
        news_data.append({
            "Title": title,
            "Paragraph": paragraph,
            "Date and Time": date_time,
            "Location": location
        })

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(news_data)

    # Save to CSV with headers and in table form
    df.to_csv("bbc_us_canada_news.csv", index=False, encoding='utf-8-sig')
    

    # Print the scraped data
    print("Scraping and saving complete! Here's the data:")
    print(df)
else:
    print(f"Failed to retrieve page {url}. Status code: {response.status_code}")
