import os
import requests
from groq import Groq
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

def get_channel_stats():
    try:
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "statistics,snippet,brandingSettings",
            "id": CHANNEL_ID,
            "key": API_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        items = data.get("items", [])
        if not items:
            return None
        item = items[0]
        stats = item.get("statistics", {})
        snippet = item.get("snippet", {})
        return {
            "name": snippet.get("title", ""),
            "description": snippet.get("description", ""),
            "subscribers": int(stats.get("subscriberCount", 0)),
            "total_views": int(stats.get("viewCount", 0)),
            "video_count": int(stats.get("videoCount", 0)),
            "created": snippet.get("publishedAt", "")
        }
    except Exception as e:
        print(f"Channel stats error: {e}")
        return None

def get_channel_videos(max_results=10):
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "channelId": CHANNEL_ID,
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
            stats_url = "https://www.googleapis.com/youtube/v3/videos"
            stats_params = {
                "part": "statistics",
                "id": video_id,
                "key": API_KEY
            }
            stats_response = requests.get(stats_url, params=stats_params, timeout=10)
            stats_data = stats_response.json()
            stats = {}
            if stats_data.get("items"):
                stats = stats_data["items"][0].get("statistics", {})
            videos.append({
                "id": video_id,
                "title": item["snippet"]["title"],
                "published": item["snippet"]["publishedAt"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "comments": int(stats.get("commentCount", 0))
            })
        return videos
    except Exception as e:
        print(f"Channel videos error: {e}")
        return []

def analyze_audience(channel_stats, videos):
    if not channel_stats and not videos:
        return None

    stats_text = f"""
Channel: {channel_stats.get('name', 'Unknown') if channel_stats else 'Unknown'}
Subscribers: {channel_stats.get('subscribers', 0):,} if channel_stats else 0
Total views: {channel_stats.get('total_views', 0):,} if channel_stats else 0
Videos: {channel_stats.get('video_count', 0)} if channel_stats else 0
"""

    videos_text = "\n".join([
        f"- {v['title']} | {v['views']:,} views | {v['likes']:,} likes"
        for v in videos[:10]
    ]) if videos else "No videos yet"

    prompt = f"""
You are a YouTube channel analyst. Analyze this channel and provide actionable intelligence.

{stats_text}

Recent videos:
{videos_text}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "channel_health": "Excellent/Good/Fair/Poor",
  "growth_stage": "New/Growing/Established/Stagnant",
  "best_performing_content": "what type of content performs best",
  "worst_performing_content": "what type underperforms",
  "posting_frequency_recommendation": "how often to post",
  "audience_insights": "who is likely watching based on content",
  "engagement_rate": "calculated engagement rate assessment",
  "top_opportunities": ["opportunity 1", "opportunity 2", "opportunity 3"],
  "immediate_actions": ["do this now 1", "do this now 2", "do this now 3"],
  "30_day_plan": "specific 30 day growth plan",
  "biggest_weakness": "main thing holding back growth",
  "biggest_strength": "main competitive advantage"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=800
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Audience analysis error: {e}")
        return None

def get_audience_intelligence():
    cache_key = "audience_intelligence"
    cached = get_cache(cache_key)
    if cached:
        return cached

    stats = get_channel_stats()
    videos = get_channel_videos()
    analysis = analyze_audience(stats, videos)

    result = {
        "channel_stats": stats,
        "recent_videos": videos,
        "analysis": analysis
    }

    set_cache(cache_key, result)
    return result