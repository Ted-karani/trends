import os
from groq import Groq
from dotenv import load_dotenv
from google_trends import get_google_trends
from cache import get_cache, set_cache
import time

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_daily_challenge(region="KE"):
    cache_key = f"challenge_{region}_{int(time.time() // 86400)}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    trends = get_google_trends(region=region)
    trends_text = "\n".join(trends[:5])

    prompt = f"""
You are a YouTube Shorts coach. Generate today's content challenge based on current trends.

Today's trends: {trends_text}
Region: {region}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "challenge_title": "catchy challenge name",
  "difficulty": "Easy/Medium/Hard",
  "trend_connection": "which trend this connects to",
  "the_challenge": "exactly what to do",
  "why_this_works": "why this type of content performs well",
  "script_starter": "first 3 lines to get started",
  "time_to_complete": "how long this should take",
  "success_metric": "how to know if you did it well",
  "pro_tip": "one insider tip to make it better",
  "example_title": "example video title"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=600
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)
        set_cache(cache_key, result)
        return result
    except Exception as e:
        print(f"Challenge error: {e}")
        return {"challenge_title": "Today's Challenge", "the_challenge": ""}