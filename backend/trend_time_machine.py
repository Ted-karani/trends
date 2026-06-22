from pytrends.request import TrendReq
from cache import get_cache, set_cache
import time

def get_historical_trends(region="KE"):
    cache_key = f"time_machine_{region}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    try:
        pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25))
        region_map = {
            "KE": "kenya", "US": "united_states",
            "GB": "united_kingdom", "NG": "nigeria"
        }
        region_name = region_map.get(region, "united_states")

        timeframes = {
            "1_year_ago": "today 12-m",
            "6_months_ago": "today 6-m",
            "3_months_ago": "today 3-m",
            "1_month_ago": "today 1-m"
        }

        historical = {}
        for label, timeframe in timeframes.items():
            try:
                time.sleep(1)
                trending = pytrends.trending_searches(pn=region_name)
                historical[label] = trending[0].tolist()[:5]
            except Exception as e:
                print(f"Time machine {label} error: {e}")
                historical[label] = []

        cycling = find_cycling_trends(historical)
        result = {"historical": historical, "cycling_trends": cycling}
        set_cache(cache_key, result)
        return result

    except Exception as e:
        print(f"Time machine error: {e}")
        return {"historical": {}, "cycling_trends": []}

def find_cycling_trends(historical):
    from groq import Groq
    import os
    import json

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    all_trends = []
    for period, trends in historical.items():
        for trend in trends:
            all_trends.append(f"[{period}] {trend}")

    if not all_trends:
        return []

    prompt = f"""
These are trends from different time periods:
{chr(10).join(all_trends)}

Identify any trends that appear to be cycling back or are likely to trend again soon.
Return ONLY a JSON array, no markdown, no backticks:

[
  {{
    "trend": "trend name",
    "last_peaked": "when it last peaked",
    "cycle_pattern": "how often it cycles",
    "comeback_likelihood": "High/Medium/Low",
    "why": "why it might come back",
    "prepare_by": "when to start preparing content"
  }}
]
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=600
        )
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Cycling trends error: {e}")
        return []