import os
import requests
from groq import Groq
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_trending_music(region="KE"):
    cache_key = f"music_{region}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    try:
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics",
            "chart": "mostPopular",
            "regionCode": region,
            "videoCategoryId": "10",
            "maxResults": 10,
            "key": API_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        songs = []
        for item in data.get("items", []):
            snippet = item["snippet"]
            stats = item.get("statistics", {})
            songs.append({
                "id": item["id"],
                "title": snippet["title"],
                "artist": snippet["channelTitle"],
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "thumbnail": snippet["thumbnails"]["high"]["url"],
                "published": snippet["publishedAt"]
            })

        analyzed = analyze_music_trends(songs)
        result = {"songs": songs, "analysis": analyzed}
        set_cache(cache_key, result)
        return result

    except Exception as e:
        print(f"Music trends error: {e}")
        return {"songs": [], "analysis": None}

def analyze_music_trends(songs):
    if not songs:
        return None

    songs_text = "\n".join([
        f"- {s['title']} by {s['artist']} ({s['views']:,} views)"
        for s in songs[:10]
    ])

    prompt = f"""
Analyze these trending music videos and identify content opportunities for a YouTube Shorts creator.

Trending songs:
{songs_text}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "hottest_song": "the single hottest song right now",
  "emerging_artist": "artist gaining momentum",
  "content_opportunities": [
    {{
      "song": "song title",
      "content_idea": "Short idea using this song",
      "hook": "hook for the Short",
      "why_now": "why post about this now"
    }}
  ],
  "genre_trends": ["genre doing well 1", "genre 2"],
  "sounds_to_use": ["sound/song to use in your Shorts 1", "sound 2", "sound 3"],
  "avoid": "any oversaturated sounds to avoid"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Music analysis error: {e}")
        return None