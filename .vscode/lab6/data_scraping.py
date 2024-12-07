import requests

API_KEY = '19ca628237754c9d8090bcb69ae1cf29'
BASE_URL = "https://newsapi.org/v2/top-headlines"


def scrape_news(country="us"):

    url = f"{BASE_URL}?country={country}&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get('articles', [])
        return [{"title": article['title'], 
                 "content": article['content'], 
                 "url": article['url']} for article in articles]
    else:
        print("Failed to fetch news:", response.status_code)
        return []
