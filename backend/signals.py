from youtube import get_trending
from google_trends import get_google_trends
from news import get_trending_news
from cache import get_cache, set_cache
import time

def calculate_velocity(video):
    try:
        from datetime import datetime, timezone
        published = video.get("published", "")
        if not published:
            return 0
        pub_time = datetime.fromisoformat(published.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        hours_old = max((now - pub_time).total_seconds() / 3600, 0.1)
        views_per_hour = video.get("views", 0) / hours_old
        return round(views_per_hour)
    except Exception as e:
        print(f"Velocity error: {e}")
        return 0

def detect_cross_platform_signals(youtube_videos, google_trends, news_articles):
    signals = []

    youtube_titles = " ".join([v.get("title", "").lower() for v in youtube_videos])
    google_terms = [t.lower() for t in google_trends]
    news_titles = " ".join([a.get("title", "").lower() for a in news_articles])

    for term in google_terms:
        term_words = term.lower().split()
        in_youtube = any(word in youtube_titles for word in term_words if len(word) > 3)
        in_news = any(word in news_titles for word in term_words if len(word) > 3)

        if in_youtube and in_news:
            signals.append({
                "term": term,
                "platforms": ["YouTube", "Google", "News"],
                "strength": "Super Trend",
                "score": 100
            })
        elif in_youtube:
            signals.append({
                "term": term,
                "platforms": ["YouTube", "Google"],
                "strength": "Strong",
                "score": 75
            })
        else:
            signals.append({
                "term": term,
                "platforms": ["Google"],
                "strength": "Emerging",
                "score": 40
            })

    return sorted(signals, key=lambda x: x["score"], reverse=True)[:10]

def get_early_signals(region="US"):
    cache_key = f"signals_{region}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    youtube = get_trending(region_code=region)
    google = get_google_trends(region=region)
    news = get_trending_news()

    for video in youtube:
        video["velocity"] = calculate_velocity(video)

    youtube_sorted = sorted(youtube, key=lambda x: x.get("velocity", 0), reverse=True)
    signals = detect_cross_platform_signals(youtube_sorted, google, news)

    result = {
        "youtube": youtube_sorted,
        "google": google,
        "news": news,
        "cross_platform_signals": signals
    }

    set_cache(cache_key, result)
    return result