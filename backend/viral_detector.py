from youtube import get_trending
from signals import calculate_velocity
from notifier import send_smart_notification
from storage import save_viral_alert, get_viral_alerts
from cache import get_cache, set_cache
import time

VIRAL_THRESHOLD = 300000

def check_for_viral_videos(region="KE"):
    try:
        videos = get_trending(region_code=region, max_results=20)
        existing_alerts = get_viral_alerts()
        existing_ids = {a["video_id"] for a in existing_alerts}

        new_viral = []
        for video in videos:
            velocity = calculate_velocity(video)
            video["velocity"] = velocity

            if velocity >= VIRAL_THRESHOLD and video["id"] not in existing_ids:
                alert = {
                    "video_id": video["id"],
                    "title": video["title"],
                    "channel": video["channel"],
                    "velocity": velocity,
                    "views": video["views"],
                    "thumbnail": video["thumbnail"],
                    "region": region
                }
                save_viral_alert(alert)
                new_viral.append(alert)

                send_smart_notification(
                    title="SUPER VIRAL ALERT",
                    message=f"{video['title']} — {velocity:,} views/hour. Post about this NOW.",
                    urgency="high"
                )
                print(f"Viral alert sent for: {video['title']}")

        return new_viral

    except Exception as e:
        print(f"Viral detector error: {e}")
        return []

def get_recent_viral_alerts():
    alerts = get_viral_alerts()
    recent = [a for a in alerts if time.time() - a.get("detected_at", 0) < 86400]
    return sorted(recent, key=lambda x: x.get("velocity", 0), reverse=True)