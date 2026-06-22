from google_trends import get_google_trends
from groq import Groq
import os
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def find_best_niches(region="KE"):
    cache_key = f"niches_{region}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    trends = get_google_trends(region=region)
    trends_text = "\n".join(trends[:15])

    prompt = f"""
You are a YouTube niche analyst. Based on these trending topics in {region}, identify the best underserved niches for a new YouTube Shorts creator.

Trending topics:
{trends_text}

Return ONLY a JSON array, no markdown, no backticks:

[
  {{
    "niche": "niche name",
    "opportunity_score": a number from 1-100,
    "competition_level": "Low/Medium/High",
    "search_volume": "Low/Medium/High/Very High",
    "why_opportunity": "why this is a good opportunity right now",
    "content_ideas": ["idea 1", "idea 2", "idea 3"],
    "monetization_potential": "Low/Medium/High",
    "time_to_grow": "realistic time to 1000 subscribers in this niche"
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
        result = json.loads(text)
        set_cache(cache_key, result)
        return result
    except Exception as e:
        print(f"Niche finder error: {e}")
        return []