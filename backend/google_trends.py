from cache import get_cache, set_cache
import requests
import time

REGION_MAP = {
    "US": "united_states",
    "KE": "kenya",
    "GB": "united_kingdom",
    "NG": "nigeria",
    "IN": "india",
    "CA": "canada",
    "AU": "australia"
}

def get_google_trends(region="US"):
    cache_key = f"google_{region}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(
            hl="en-US",
            tz=360,
            timeout=(10, 25),
            retries=3,
            backoff_factor=1.0,
            requests_args={"verify": False}
        )
        region_name = REGION_MAP.get(region, "united_states")
        time.sleep(2)
        trending = pytrends.trending_searches(pn=region_name)
        results = trending[0].tolist()[:10]
        if results:
            set_cache(cache_key, results)
        return results
    except Exception as e:
        print(f"Google Trends error: {e}")
        return get_fallback_trends(region)

def get_fallback_trends(region="US"):
    try:
        url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={region}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            import re
            titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', response.text)
            results = [t for t in titles if t != "Daily Search Trends"][:10]
            if results:
                return results
    except Exception as e:
        print(f"Fallback trends error: {e}")
    return []