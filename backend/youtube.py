import requests
import os
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

CATEGORIES = {
    "0": "All",
    "10": "Music",
    "20": "Gaming",
    "25": "News",
    "17": "Sports",
    "28": "Science & Tech"
}

def get_trending(category_id="0", region_code="US", max_results=10):
    cache_key = f"youtube_{category_id}_{region_code}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region_code,
        "videoCategoryId": category_id,
        "maxResults": max_results,
        "key": API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if "items" not in data:
            print(f"YouTube API error: {data}")
            return []

        videos = []
        for item in data["items"]:
            snippet = item["snippet"]
            stats = item.get("statistics", {})
            videos.append({
                "id": item["id"],
                "title": snippet["title"],
                "channel": snippet["channelTitle"],
                "thumbnail": snippet["thumbnails"]["high"]["url"],
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "published": snippet["publishedAt"],
                "description": snippet.get("description", "")[:200],
                "category": CATEGORIES.get(category_id, "All")
            })

        set_cache(cache_key, videos)
        return videos

    except Exception as e:
        print(f"YouTube error: {e}")
        return []