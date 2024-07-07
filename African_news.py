import pandas as pd
import requests
import csv
import os.path

# Set up logging to CSV file
log_file = 'load_data.csv'
log_columns = ['timestamp', 'level', 'link']

# Create the CSV log file if it doesn't exist and write the header
if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(log_columns)

# Function to log messages to the CSV file
def log_to_csv(level, link):
    timestamp = pd.Timestamp.now()
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, level, link])

# Function to scrape BBC Africa news
def scrape_bbc_africa_news():
    url = "https://web-cdn.api.bbci.co.uk/xd/content-collection/f7905f4a-3031-4e07-ac0c-ad31eeb6a08e?country=ke&page=0"
    try:
        response = requests.get(url)
        log_to_csv('INFO', url)  # Adjusted to pass 'INFO' and the URL

        if response.status_code == 200:
            data = response.json()
            news_items = data.get('data', [])

            # Prepare data lists
            news_data = []
            for item in news_items:
                title = item.get('title', '')
                date = item.get('firstPublishedAt', '')
                summary = item.get('summary', '')
                link = f"https://www.bbc.com{item.get('path', '')}"

                # Append data to list
                news_data.append([date, title, summary, link])
                log_to_csv('INFO', link)  # Logging each news item's link

            # Create DataFrame
            df = pd.DataFrame(news_data, columns=['date', 'title', 'summary', 'link'])

            # Save DataFrame to CSV file
            filename = "africa_news.csv"
            if not os.path.exists(filename):
                df.to_csv(filename, index=False)
            else:
                df.to_csv(filename, mode='a', index=False, header=False)

            log_to_csv('INFO', f"Data saved to '{filename}'")

        else:
            log_to_csv('ERROR', f"Failed to fetch BBC Africa news. Status code: {response.status_code}")

    except requests.RequestException as e:
        log_to_csv('ERROR', f"Error fetching BBC Africa news: {e}")

# Execute scraping function
scrape_bbc_africa_news()
