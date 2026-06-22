import requests
from groq import Groq
import os
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LANGUAGE_REGIONS = {
    "swahili": "KE",
    "french": "FR",
    "portuguese": "BR",
    "spanish": "MX"
}

def get_foreign_trends():
    cache_key = "cross_language_trends"
    cached = get_cache(cache_key)
    if cached:
        return cached

    try:
        from pytrends.request import TrendReq
        import time

        all_trends = {}
        pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25))

        for language, region in LANGUAGE_REGIONS.items():
            try:
                time.sleep(1)
                trending = pytrends.trending_searches(pn=region.lower() if region != "BR" else "brazil")
                all_trends[language] = trending[0].tolist()[:5]
            except Exception as e:
                print(f"Cross language {language} error: {e}")
                all_trends[language] = []

        if any(all_trends.values()):
            analyzed = analyze_foreign_trends(all_trends)
            result = {"trends": all_trends, "analysis": analyzed}
            set_cache(cache_key, result)
            return result

        return {"trends": all_trends, "analysis": []}

    except Exception as e:
        print(f"Cross language error: {e}")
        return {"trends": {}, "analysis": []}

def analyze_foreign_trends(trends_by_language):
    all_trends = []
    for lang, trends in trends_by_language.items():
        for trend in trends:
            all_trends.append(f"[{lang}] {trend}")

    if not all_trends:
        return []

    prompt = f"""
You are a global trend analyst. These are trending topics in different languages right now:

{chr(10).join(all_trends)}

Identify which of these are likely to cross over into English speaking markets soon and why.
Return ONLY a JSON array, no markdown, no backticks:

[
  {{
    "trend": "the trend",
    "language": "original language",
    "crossover_potential": "High/Medium/Low",
    "reason": "why it might cross over",
    "english_angle": "how an English creator could cover this now before it crosses over",
    "timeframe": "when it might hit English markets"
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
        print(f"Analysis error: {e}")
        return []