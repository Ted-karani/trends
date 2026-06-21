from pytrends.request import TrendReq
from cache import get_cache, set_cache
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
        pytrends = TrendReq(
            hl="en-US",
            tz=360,
            timeout=(10, 25),
            retries=2,
            backoff_factor=0.5
        )
        region_name = REGION_MAP.get(region, "united_states")
        time.sleep(1)
        trending = pytrends.trending_searches(pn=region_name)
        results = trending[0].tolist()[:10]
        if results:
            set_cache(cache_key, results)
        return results
    except Exception as e:
        print(f"Google Trends error: {e}")
        return []