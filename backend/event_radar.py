import os
import requests
from groq import Groq
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")

def get_upcoming_matches():
    try:
        headers = {"X-Auth-Token": FOOTBALL_API_KEY}
        url = "https://api.football-data.org/v4/matches"
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        matches = []
        for match in data.get("matches", [])[:10]:
            matches.append({
                "home": match["homeTeam"]["name"],
                "away": match["awayTeam"]["name"],
                "competition": match["competition"]["name"],
                "date": match["utcDate"],
                "status": match["status"]
            })
        return matches
    except Exception as e:
        print(f"Football API error: {e}")
        return []

def get_live_matches():
    try:
        headers = {"X-Auth-Token": FOOTBALL_API_KEY}
        url = "https://api.football-data.org/v4/matches?status=LIVE"
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        matches = []
        for match in data.get("matches", []):
            matches.append({
                "home": match["homeTeam"]["name"],
                "away": match["awayTeam"]["name"],
                "score": f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}",
                "competition": match["competition"]["name"],
                "minute": match.get("minute", ""),
                "status": match["status"]
            })
        return matches
    except Exception as e:
        print(f"Live matches error: {e}")
        return []

def generate_event_content_ideas(events_text, region="KE"):
    prompt = f"""
You are a sports content strategist. Based on these upcoming events generate YouTube Shorts content ideas.

Events: {events_text}
Region: {region}

Return ONLY a JSON array, no markdown, no backticks:

[
  {{
    "event": "event name",
    "content_idea": "specific Short idea",
    "hook": "opening hook",
    "best_time_to_post": "when to post relative to the event",
    "predicted_views": "view estimate",
    "angle": "unique angle"
  }}
]
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Event ideas error: {e}")
        return []

def get_event_radar(region="KE"):
    cache_key = f"events_{region}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    upcoming = get_upcoming_matches()
    live = get_live_matches()

    events_text = "\n".join([
        f"{m['home']} vs {m['away']} - {m['competition']} - {m['date']}"
        for m in upcoming[:5]
    ])

    ideas = generate_event_content_ideas(events_text, region) if events_text else []

    result = {
        "upcoming_matches": upcoming,
        "live_matches": live,
        "content_ideas": ideas
    }

    set_cache(cache_key, result)
    return result