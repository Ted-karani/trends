import requests
from pytrends.request import TrendReq
from cache import get_cache, set_cache
import time

def get_autocomplete_suggestions(query):
    try:
        url = f"https://suggestqueries.google.com/complete/search"
        params = {
            "client": "youtube",
            "ds": "yt",
            "q": query
        }
        response = requests.get(url, params=params, timeout=10)
        suggestions = response.json()[1]
        return [s[0] for s in suggestions[:5]]
    except Exception as e:
        print(f"Autocomplete error: {e}")
        return []

def get_search_interest(keywords):
    try:
        pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25))
        time.sleep(1)
        pytrends.build_payload(keywords[:5], timeframe="now 1-d")
        interest = pytrends.interest_over_time()
        if interest.empty:
            return {}
        latest = interest.iloc[-1]
        return {kw: int(latest.get(kw, 0)) for kw in keywords[:5]}
    except Exception as e:
        print(f"Search interest error: {e}")
        return {}

def estimate_search_volume(topic):
    cache_key = f"search_{topic[:30]}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    try:
        suggestions = get_autocomplete_suggestions(topic)
        interest = get_search_interest([topic])
        score = interest.get(topic, 0)

        if score >= 75:
            volume_label = "Exploding"
            volume_score = 95
        elif score >= 50:
            volume_label = "Very High"
            volume_score = 75
        elif score >= 25:
            volume_label = "High"
            volume_score = 50
        elif score >= 10:
            volume_label = "Medium"
            volume_score = 25
        else:
            volume_label = "Low"
            volume_score = 10

        result = {
            "topic": topic,
            "volume_label": volume_label,
            "volume_score": volume_score,
            "related_searches": suggestions,
            "trend_score": score
        }

        set_cache(cache_key, result)
        return result

    except Exception as e:
        print(f"Search volume error: {e}")
        return {
            "topic": topic,
            "volume_label": "Unknown",
            "volume_score": 0,
            "related_searches": [],
            "trend_score": 0
        }