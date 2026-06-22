from youtube import get_trending
from google_trends import get_google_trends
from news import get_trending_news
from signals import get_early_signals, calculate_velocity
from cache import get_cache, set_cache
from storage import save_trend_history
import time

def get_live_trends(region="KE"):
    cache_key = f"live_{region}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    try:
        youtube = get_trending(region_code=region)
        google = get_google_trends(region=region)
        news = get_trending_news()
        signals = get_early_signals(region=region)

        for video in youtube:
            video["velocity"] = calculate_velocity(video)

        youtube_sorted = sorted(youtube, key=lambda x: x.get("velocity", 0), reverse=True)

        spikes = []
        for video in youtube_sorted[:5]:
            velocity = video.get("velocity", 0)
            if velocity > 50000:
                spike = {
                    "title": video["title"],
                    "channel": video["channel"],
                    "velocity": velocity,
                    "views": video["views"],
                    "thumbnail": video["thumbnail"],
                    "id": video["id"],
                    "spike_level": "Extreme" if velocity > 500000 else "High" if velocity > 100000 else "Medium"
                }
                spikes.append(spike)
                save_trend_history({
                    "title": video["title"],
                    "views": video["views"],
                    "velocity": velocity,
                    "region": region
                })

        result = {
            "spikes": spikes,
            "youtube": youtube_sorted[:10],
            "google": google[:10],
            "news": news[:5],
            "cross_platform": signals.get("cross_platform_signals", [])[:5],
            "last_updated": time.time()
        }

        set_cache(cache_key, result)
        return result

    except Exception as e:
        print(f"Live trends error: {e}")
        return {
            "spikes": [],
            "youtube": [],
            "google": [],
            "news": [],
            "cross_platform": [],
            "last_updated": time.time()
        }