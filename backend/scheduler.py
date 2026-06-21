from apscheduler.schedulers.background import BackgroundScheduler
from youtube import get_trending
from google_trends import get_google_trends
from reddit import get_reddit_trends
from summarizer import summarize_trends
from notifier import notify_trending
from cache import clear_cache

def fetch_and_notify(region="US", category="0"):
    print("Clearing cache...")
    clear_cache()

    print("Fetching from all sources...")
    youtube = get_trending(category_id=category, region_code=region)
    google = get_google_trends(region=region)
    reddit = get_reddit_trends()

    print("Summarizing with AI...")
    summary = summarize_trends(youtube, google, reddit)

    print("Sending notification...")
    notify_trending(summary)

    print(f"Done!")
    return summary

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        fetch_and_notify,
        "interval",
        hours=3,
        id="trend_fetch"
    )
    scheduler.start()
    print("Scheduler started — fetching every 3 hours")
    return scheduler