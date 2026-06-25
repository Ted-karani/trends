import os
from groq import Groq
from dotenv import load_dotenv
from google_trends import get_google_trends
from news import get_trending_news
from cache import get_cache, set_cache

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_content_calendar(region="KE"):
    cache_key = f"calendar_{region}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    trends = get_google_trends(region=region)
    news = get_trending_news()

    trends_text = "\n".join(trends[:10])
    news_text = "\n".join([a["title"] for a in news[:5]])

    prompt = f"""
You are a YouTube Shorts content calendar strategist.

Current trends: {trends_text}
Current news: {news_text}
Region: {region}

Create a 7-day content calendar. Return ONLY a JSON array, no markdown, no backticks:

[
  {{
    "day": "Monday",
    "date": "Day 1",
    "topic": "content topic",
    "angle": "specific angle to take",
    "hook": "opening hook",
    "best_time": "best posting time",
    "urgency": "High/Medium/Low",
    "predicted_views": "view estimate",
    "type": "Explainer/Reaction/List/Challenge/News"
  }}
]
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1200
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)
        set_cache(cache_key, result)
        return result
    except Exception as e:
        print(f"Calendar error: {e}")
        return []