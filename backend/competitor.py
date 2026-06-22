import requests
import os
from dotenv import load_dotenv
from storage import get_competitor_channels
from cache import get_cache, set_cache

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_channel(query):
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "channel",
            "maxResults": 5,
            "key": API_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        channels = []
        for item in data.get("items", []):
            channels.append({
                "id": item["id"]["channelId"],
                "name": item["snippet"]["title"],
                "description": item["snippet"]["description"][:100],
                "thumbnail": item["snippet"]["thumbnails"]["default"]["url"]
            })
        return channels
    except Exception as e:
        print(f"Channel search error: {e}")
        return []

def get_channel_recent_videos(channel_id, max_results=5):
    cache_key = f"competitor_{channel_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "order": "date",
            "maxResults": max_results,
            "type": "video",
            "key": API_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        videos = []
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            stats = get_video_stats(video_id)
            videos.append({
                "id": video_id,
                "title": item["snippet"]["title"],
                "published": item["snippet"]["publishedAt"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "views": stats.get("views", 0),
                "likes": stats.get("likes", 0)
            })

        set_cache(cache_key, videos)
        return videos
    except Exception as e:
        print(f"Competitor videos error: {e}")
        return []

def get_video_stats(video_id):
    try:
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "statistics",
            "id": video_id,
            "key": API_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        items = data.get("items", [])
        if items:
            stats = items[0].get("statistics", {})
            return {
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0))
            }
        return {"views": 0, "likes": 0}
    except:
        return {"views": 0, "likes": 0}

def get_all_competitor_data():
    channels = get_competitor_channels()
    if not channels:
        return []

    competitor_data = []
    for channel in channels:
        videos = get_channel_recent_videos(channel["id"])
        if videos:
            top_video = max(videos, key=lambda x: x.get("views", 0))
            competitor_data.append({
                "channel": channel,
                "recent_videos": videos,
                "top_video": top_video,
                "total_views": sum(v.get("views", 0) for v in videos)
            })

    return sorted(competitor_data, key=lambda x: x["total_views"], reverse=True)