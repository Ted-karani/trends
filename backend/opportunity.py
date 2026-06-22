from signals import get_early_signals, calculate_velocity
from search_volume import estimate_search_volume
from cache import get_cache, set_cache
import time

def score_opportunity(video, signals, region="US"):
    score = 0
    urgency = "Watch"
    reasons = []

    velocity = video.get("velocity", 0)
    if velocity > 500000:
        score += 40
        reasons.append("Exploding views per hour")
    elif velocity > 100000:
        score += 25
        reasons.append("Very high velocity")
    elif velocity > 50000:
        score += 15
        reasons.append("High velocity")

    views = video.get("views", 0)
    likes = video.get("likes", 0)
    if views > 0:
        like_ratio = (likes / views) * 100
        if like_ratio > 8:
            score += 20
            reasons.append("Exceptional engagement")
        elif like_ratio > 5:
            score += 10
            reasons.append("Strong engagement")

    title_lower = video.get("title", "").lower()
    for signal in signals:
        signal_words = signal.get("term", "").lower().split()
        if any(word in title_lower for word in signal_words if len(word) > 3):
            if signal.get("strength") == "Super Trend":
                score += 30
                reasons.append("Super trend across all platforms")
            elif signal.get("strength") == "Strong":
                score += 20
                reasons.append("Trending on multiple platforms")

    if score >= 80:
        urgency = "Post Now"
    elif score >= 60:
        urgency = "Post Today"
    elif score >= 40:
        urgency = "Post This Week"
    else:
        urgency = "Watch"

    return {
        "score": min(score, 100),
        "urgency": urgency,
        "reasons": reasons
    }

def get_opportunities(region="US"):
    cache_key = f"opportunities_{region}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    try:
        signals_data = get_early_signals(region=region)
        youtube_videos = signals_data.get("youtube", [])
        signals = signals_data.get("cross_platform_signals", [])

        opportunities = []
        for video in youtube_videos[:15]:
            scoring = score_opportunity(video, signals, region)
            time.sleep(0.1)

            opportunities.append({
                **video,
                "opportunity_score": scoring["score"],
                "urgency": scoring["urgency"],
                "reasons": scoring["reasons"]
            })

        opportunities_sorted = sorted(
            opportunities,
            key=lambda x: x["opportunity_score"],
            reverse=True
        )

        post_now = [o for o in opportunities_sorted if o["urgency"] == "Post Now"]
        post_today = [o for o in opportunities_sorted if o["urgency"] == "Post Today"]
        post_week = [o for o in opportunities_sorted if o["urgency"] == "Post This Week"]
        watch = [o for o in opportunities_sorted if o["urgency"] == "Watch"]

        result = {
            "post_now": post_now,
            "post_today": post_today,
            "post_week": post_week,
            "watch": watch,
            "signals": signals,
            "all": opportunities_sorted
        }

        set_cache(cache_key, result)
        return result

    except Exception as e:
        print(f"Opportunity error: {e}")
        return {
            "post_now": [],
            "post_today": [],
            "post_week": [],
            "watch": [],
            "signals": [],
            "all": []
        }