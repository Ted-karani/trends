from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from youtube import get_trending
from google_trends import get_google_trends
from news import get_trending_news
from signals import get_early_signals
from opportunity import get_opportunities
from summarizer import summarize_trends
from notifier import notify_trending, send_smart_notification
from cache import clear_cache

def fetch_and_notify(region="KE", category="0"):
    print("Clearing cache...")
    clear_cache()

    print("Fetching from all sources...")
    youtube = get_trending(category_id=category, region_code=region)
    google = get_google_trends(region=region)
    news = get_trending_news()

    print("Getting opportunities...")
    opportunities = get_opportunities(region=region)
    post_now = opportunities.get("post_now", [])

    print("Summarizing with AI...")
    summary = summarize_trends(youtube, google, [], news)

    print("Sending notification...")
    if post_now:
        top = post_now[0]
        send_smart_notification(
            title="Post Now - Trend Alert",
            message=f"{top['title']} - Score: {top['opportunity_score']}/100. {summary[:200]}",
            urgency="high"
        )
    else:
        notify_trending(summary)

    print("Done!")
    return summary

def morning_briefing_job():
    print("Sending morning briefing...")
    from briefing import generate_morning_briefing
    from notifier import send_smart_notification
    briefing = generate_morning_briefing(region="KE")
    top_3 = briefing.get("top_3", [])
    if top_3:
        topics = ", ".join([t["topic"] for t in top_3])
        send_smart_notification(
            title="Morning Briefing - Top Trends",
            message=f"Today's top 3: {topics}. {briefing.get('motivation', '')}",
            urgency="default"
        )

def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        fetch_and_notify,
        "interval",
        hours=3,
        id="trend_fetch"
    )

    scheduler.add_job(
        morning_briefing_job,
        CronTrigger(hour=8, minute=0),
        id="morning_briefing"
    )

    scheduler.start()
    print("Scheduler started")
    return scheduler