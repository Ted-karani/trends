from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from youtube import get_trending, CATEGORIES
from google_trends import get_google_trends
from reddit import get_reddit_trends
from summarizer import summarize_trends
from notifier import notify_trending
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
def trending(category="0", region="US"):
    videos = get_trending(category_id=category, region_code=region)
    return {"videos": videos, "category": CATEGORIES.get(category, "All")}

@app.get("/categories")
def categories():
    return CATEGORIES

@app.get("/summary")
def summary(category="0", region="US"):
    youtube = get_trending(category_id=category, region_code=region)
    google = get_google_trends(region=region)
    reddit = get_reddit_trends()
    ai_summary = summarize_trends(youtube, google, reddit)
    return {"summary": ai_summary}

@app.get("/notify")
def notify(category="0", region="US"):
    result = fetch_and_notify(region=region, category=category)
    return {"status": "Notification sent!", "summary": result}

@app.get("/google-trends")
def google_trends(region="US"):
    trends = get_google_trends(region=region)
    return {"trends": trends}

@app.get("/reddit-trends")
def reddit_trends():
    posts = get_reddit_trends()
    return {"posts": posts}

@app.get("/refresh")
def refresh():
    clear_cache()
    return {"status": "Cache cleared!"}