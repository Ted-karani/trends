import os
import requests
from groq import Groq
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_youtube(query, max_results=10):
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "order": "viewCount",
            "maxResults": max_results,
            "key": API_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        videos = []
        for item in data.get("items", []):
            videos.append({
                "id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "published": item["snippet"]["publishedAt"]
            })
        return videos
    except Exception as e:
        print(f"Search error: {e}")
        return []

def find_untapped_opportunities(region="KE"):
    cache_key = f"search_spy_{region}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    from google_trends import get_google_trends
    trends = get_google_trends(region=region)

    opportunities = []
    for trend in trends[:8]:
        videos = search_youtube(trend, max_results=5)
        video_count = len(videos)

        if video_count <= 3:
            difficulty = "Very Easy"
            score = 95
        elif video_count <= 6:
            difficulty = "Easy"
            score = 80
        elif video_count <= 10:
            difficulty = "Medium"
            score = 60
        else:
            difficulty = "Hard"
            score = 30

        opportunities.append({
            "topic": trend,
            "video_count": video_count,
            "difficulty": difficulty,
            "opportunity_score": score,
            "existing_videos": videos[:3]
        })

    opportunities_sorted = sorted(
        opportunities,
        key=lambda x: x["opportunity_score"],
        reverse=True
    )

    set_cache(cache_key, opportunities_sorted)
    return opportunities_sorted