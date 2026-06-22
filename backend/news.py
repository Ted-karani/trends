import requests
import os
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_trending_news():
    cache_key = "news_trends"
    cached = get_cache(cache_key)
    if cached:
        return cached

    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "pageSize": 10
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") != "ok":
            print(f"News API error: {data}")
            return []

        articles = []
        for article in data.get("articles", []):
            if article.get("title") and article.get("title") != "[Removed]":
                articles.append({
                    "title": article.get("title", ""),
                    "source": article.get("source", {}).get("name", ""),
                    "url": article.get("url", ""),
                    "published": article.get("publishedAt", ""),
                    "description": article.get("description", "")[:200] if article.get("description") else ""
                })

        if articles:
            set_cache(cache_key, articles)
        return articles

    except Exception as e:
        print(f"News error: {e}")
        return []