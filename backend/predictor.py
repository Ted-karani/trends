from storage import get_trend_history
from groq import Groq
import os
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def predict_upcoming_trends(current_trends, region="KE"):
    cache_key = f"predictions_{region}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    history = get_trend_history()
    history_text = "\n".join([
        f"- {h['title']} | views: {h.get('views', 0):,} | velocity: {h.get('velocity', 0):,}/hr"
        for h in history[-50:]
    ]) if history else "No history yet"

    current_text = "\n".join([
        f"- {t}" for t in current_trends[:10]
    ])

    prompt = f"""
You are a trend prediction AI. Based on current trends and historical patterns, predict what will trend next.

Current trends:
{current_text}

Historical trend data:
{history_text}

Region: {region}

Predict upcoming trends. Return ONLY a JSON array, no markdown, no backticks:

[
  {{
    "predicted_trend": "what will trend",
    "confidence": "High/Medium/Low",
    "timeframe": "when it will peak (hours/days)",
    "reason": "why you predict this",
    "content_opportunity": "how to get ahead of it",
    "related_to": "what current trend this connects to"
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
        print(f"Predictor error: {e}")
        return []