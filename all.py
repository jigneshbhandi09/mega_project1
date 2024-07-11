import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_bbc_africa_news():
    base_url = "https://web-cdn.api.bbci.co.uk/xd/content-collection/f7905f4a-3031-4e07-ac0c-ad31eeb6a08e?country=ke&page={}"
    news_data = []
    
    for page in range(10):  # Iterate over 10 pages
        url = base_url.format(page)
        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                news_items = data.get('data', [])

                for item in news_items:
                    title = item.get('title', '')
                    date = item.get('firstPublishedAt', '')
                    link = f"https://www.bbc.com{item.get('path', '')}"
                    
                    # Append data to list
                    news_data.append([date, title, link])

            else:
                print(f"Failed to fetch BBC Africa news for page {page}. Status code: {response.status_code}")

        except requests.RequestException as e:
            print(f"Error fetching BBC Africa news for page {page}: {e}")
    
    # Create DataFrame
    df = pd.DataFrame(news_data, columns=['Date', 'Title', 'Link'])

    # Display data in tabular format
    print(df)

    # Save DataFrame to CSV file
    filename = "africa_news.csv"
    df.to_csv(filename, index=False)
    print(f"Data saved to '{filename}'")

def scrape_south_america_news():
    url = 'https://apnews.com/hub/south-america'  
    country = "South America"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        news_articles = []

        articles = soup.findAll('div', class_='PagePromo-content')

        for article in articles:
            next_part = article.find('a', class_='Link')
            page_url = next_part.get('href')
            title = next_part.find('span', class_='PagePromoContentIcons-text').text

            timestamp_element = article.find('bsp-timestamp')
            if timestamp_element:
                timestamp = timestamp_element.get('data-timestamp')
                # Convert timestamp to datetime object
                date = datetime.utcfromtimestamp(int(timestamp) / 1000).strftime('%Y-%m-%d')

            response = requests.get(page_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                try:
                    categories = soup.find('div', class_='Page-breadcrumbs').text.strip()
                except:
                    categories = "other"
                    
                news_articles.append({
                    'date': date,
                    'location': 'South America',
                    'title': title,
                    'categories': categories,
                    'source_link': page_url,
                    'country': country  # Add country information
                })

        return news_articles
    else:
        print(f"Failed to retrieve page: {response.status_code}")

def scrape_ndtv_asia_news():
    url_base = "https://www.ndtv.com/world/asia/page-"
    news_title = []
    news_date = []
    news_location = []
    news_url = []

    # Adjust the range as per the number of pages you want to scrape
    for page_num in range(1, 15):  # Scraping pages 1 to 14
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

def scrape_ndtv_australia_news():
    url_base = "https://www.ndtv.com/world/australia/page-"
    news_title = []
    news_date = []
    news_location = []
    news_url = []

    for page_num in range(1, 11):  # Scraping pages 1 to 10
        url = url_base + str(page_num)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        news_data = soup.find("div", class_="lisingNews")
        news_aust = news_data.find_all("div", class_="news_Itm")

        for latest in news_aust:
            try:
                updated = latest.find("div", class_="news_Itm-cont")
                date_time = updated.find("span").text.split("|")[1]
                date = date_time.split(",")
                try:
                    tit = updated.find("h2", class_="newsHdng")
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
                    link = tit.find('a')
                    news_url.append(link.get('href'))
                except:
                    news_url.append(" ")
            except:
                pass

    dic = {
        "urls": news_url,
        "date": news_date,
        "location": news_location,
        "title": news_title
    }

    df = pd.DataFrame(dic)
    df.to_csv("news_australia.csv", index=False)

    print("Scraping and saving complete!")

def scrape_bbc_us_canada_news():
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
                title_element = item.find("h2", {"data-testid": "card-headline"})
                title = title_element.get_text().strip() if title_element else ""
                
                # Extract URL if title element exists
                url = title_element.find_parent('a')['href'] if title_element and title_element.find_parent('a') else ""
                if url and not url.startswith("http"):
                    url = "https://www.bbc.com" + url  # Ensure full URL
            except AttributeError:
                title = ""
                url = ""

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
                "Location": location,
                "URL": url
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

def scrape_bbc_us_europe_news():
    # URL of the BBC Europe news page
    URL = "https://www.bbc.com/news/world/europe"

    # Send a GET request to the webpage
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # List to hold data for each article
    data = []

    # Find all articles on the page
    articles = soup.find_all('div', class_='sc-b8778340-0 kFuHJG')
    
    if not articles:
        print("No articles found")
    else:
        for article in articles:
            try:
                # Extract the title
                title_tag = article.find('h2',class_='sc-4fedabc7-3 zTZri')
                title = title_tag.text.strip() if title_tag else 'No title available'

                # Extract the summary
                summary_tag = article.find('p',class_='sc-b8778340-4 kYtujW')
                summary = summary_tag.text.strip() if summary_tag else 'No summary available'

                # Extract the category
                category_tag = article.find('div', class_='sc-4e537b1-2 eRsxHt')
                category = category_tag.text.strip() if category_tag else 'No category available'

                # Extract the publication date
                date_tag = article.find('div', class_='sc-4e537b1-1 dsUUMv')
                date = date_tag['datetime'] if date_tag else datetime.now().strftime('%Y-%m-%d')

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
    save_to_csv(data, filename='europe_news.csv')

def scrape_bbc_us_world_news():
    url="https://www.ndtv.com/world/asia/page-"
    news_title=[]
    news_date=[]
    news_location=[]
    news_url=[]

    for i in range(1,11):
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
                    link=tit.find('a')
                    news_url.append(link.get('href'))
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
    df.to_csv("news_world.csv")

def save_to_csv(data, filename):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save")

def main():
    while True:
        print("Choose an option:")
        print("1. Scrape BBC Africa News")
        print("2. Scrape South America News")
        print("3. Scrape NDTV Asia News")
        print("4. Scrape NDTV Australia News")
        print("5. Scrape BBC US & Canada News")
        print("6. Scrape BBC US & Europe News")
        print("7. Scrape BBC US World News")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            scrape_bbc_africa_news()
        elif choice == '2':
            south_america_news = scrape_south_america_news()
            save_to_csv(south_america_news, 'south_america_news.csv')  # Corrected function name
        elif choice == '3':
            scrape_ndtv_asia_news()
        elif choice == '4':
            scrape_ndtv_australia_news()
        elif choice == '5':
            scrape_bbc_us_canada_news()
        elif choice == '6':
            scrape_bbc_us_europe_news()
        elif choice == '7':
            scrape_bbc_us_world_news()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
