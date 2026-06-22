import os
from groq import Groq
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_trend_sentiment(trend_title, context=""):
    cache_key = f"sentiment_{trend_title[:30]}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    prompt = f"""
Analyze the sentiment and mood around this trending topic: "{trend_title}"
Context: {context}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "overall_sentiment": "Positive/Negative/Neutral/Mixed/Controversial",
  "mood": "the dominant emotion (hype/funny/angry/sad/inspiring/shocking)",
  "phase": "which phase is this trend in (emerging/rising/peak/declining/dead)",
  "safe_to_post": true or false,
  "tone_recommendation": "what tone to use when making content about this",
  "sentiment_score": a number from -100 (very negative) to 100 (very positive),
  "controversy_risk": "Low/Medium/High",
  "audience_emotion": "what emotion this triggers in viewers",
  "best_angle": "the safest and most engaging angle to take on this trend"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=400
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)
        set_cache(cache_key, result)
        return result
    except Exception as e:
        print(f"Sentiment error: {e}")
        return {
            "overall_sentiment": "Unknown",
            "mood": "neutral",
            "phase": "unknown",
            "safe_to_post": True,
            "tone_recommendation": "neutral tone",
            "sentiment_score": 0,
            "controversy_risk": "Low",
            "audience_emotion": "neutral",
            "best_angle": "informational"
        }