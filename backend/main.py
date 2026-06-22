from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from youtube import get_trending, CATEGORIES
from google_trends import get_google_trends
from news import get_trending_news
from signals import get_early_signals
from opportunity import get_opportunities
from content_engine import generate_content_package
from producer import get_production_guide
from briefing import generate_morning_briefing
from search_volume import estimate_search_volume
from summarizer import summarize_trends
from notifier import notify_trending, send_smart_notification
from scheduler import start_scheduler, fetch_and_notify
from cache import clear_cache
import os

app = FastAPI()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

scheduler = start_scheduler()

@app.get("/")
def root():
    return {"status": "Trend Radar is running!"}

@app.get("/trending")
def trending(category="0", region="KE"):
    videos = get_trending(category_id=category, region_code=region)
    return {"videos": videos, "category": CATEGORIES.get(category, "All")}

@app.get("/categories")
def categories():
    return CATEGORIES

@app.get("/opportunities")
def opportunities(region="KE"):
    return get_opportunities(region=region)

@app.get("/signals")
def signals(region="KE"):
    return get_early_signals(region=region)

@app.get("/news")
def news():
    return {"articles": get_trending_news()}

@app.get("/summary")
def summary(category="0", region="KE"):
    youtube = get_trending(category_id=category, region_code=region)
    google = get_google_trends(region=region)
    news_data = get_trending_news()
    ai_summary = summarize_trends(youtube, google, [], news_data)
    return {"summary": ai_summary}

@app.get("/content-package")
def content_package(video_id: str, region="KE"):
    youtube = get_trending(region_code=region)
    video = next((v for v in youtube if v["id"] == video_id), None)
    if not video:
        return {"error": "Video not found"}
    package = generate_content_package(video, region=region)
    return {"package": package, "video": video}

@app.get("/production-guide")
def production_guide(video_id: str, region="KE"):
    youtube = get_trending(region_code=region)
    video = next((v for v in youtube if v["id"] == video_id), None)
    if not video:
        return {"error": "Video not found"}
    package = generate_content_package(video, region=region)
    guide = get_production_guide(video, package)
    return {"guide": guide, "package": package, "video": video}

@app.get("/briefing")
def briefing(region="KE"):
    return generate_morning_briefing(region=region)

@app.get("/search-volume")
def search_volume(topic: str):
    return estimate_search_volume(topic)

@app.get("/google-trends")
def google_trends(region="KE"):
    trends = get_google_trends(region=region)
    return {"trends": trends}

@app.get("/notify")
def notify(category="0", region="KE"):
    result = fetch_and_notify(region=region, category=category)
    return {"status": "Notification sent!", "summary": result}

@app.get("/refresh")
def refresh():
    clear_cache()
    return {"status": "Cache cleared!"}