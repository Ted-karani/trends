from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
from live_trends import get_live_trends
from viral_detector import check_for_viral_videos, get_recent_viral_alerts
from localization import localize_trend
from cross_language import get_foreign_trends
from sentiment_tracker import analyze_trend_sentiment
from trend_time_machine import get_historical_trends
from script_improver import improve_script
from repurposer import repurpose_content
from hook_database import generate_and_save_hooks, get_best_hooks
from search_intent import analyze_search_intent
from competitor import search_channel, get_channel_recent_videos, get_all_competitor_data
from predictor import predict_upcoming_trends
from growth_simulator import simulate_growth
from niche_finder import find_best_niches
from monetization import get_monetization_insights
from collab_finder import find_collab_opportunities
from lifecycle import analyze_trend_lifecycle
from api_monitor import get_full_health_report
from video_blueprint import generate_video_blueprint
from storage import (
    add_competitor_channel, remove_competitor_channel,
    get_competitor_channels, save_hook
)
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

class ScriptRequest(BaseModel):
    script: str
    niche: str = "general"

class RepurposeRequest(BaseModel):
    video_title: str
    video_description: str = ""
    niche: str = "general"

class GrowthRequest(BaseModel):
    subscribers: int = 0
    avg_views: int = 0
    posts_per_week: int = 1
    niche: str = "general"

class CollabRequest(BaseModel):
    niche: str = "general"
    subscribers: int = 0

class ChannelRequest(BaseModel):
    id: str
    name: str
    description: str = ""
    thumbnail: str = ""

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
        raise HTTPException(status_code=404, detail="Video not found")
    package = generate_content_package(video, region=region)
    return {"package": package, "video": video}

@app.get("/production-guide")
def production_guide(video_id: str, region="KE"):
    youtube = get_trending(region_code=region)
    video = next((v for v in youtube if v["id"] == video_id), None)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    package = generate_content_package(video, region=region)
    guide = get_production_guide(video, package)
    blueprint = generate_video_blueprint(video, package)
    return {"guide": guide, "package": package, "video": video, "blueprint": blueprint}

@app.get("/briefing")
def briefing(region="KE"):
    return generate_morning_briefing(region=region)

@app.get("/search-volume")
def search_volume(topic: str):
    return estimate_search_volume(topic)

@app.get("/google-trends")
def google_trends(region="KE"):
    return {"trends": get_google_trends(region=region)}

@app.get("/live-trends")
def live_trends(region="KE"):
    return get_live_trends(region=region)

@app.get("/viral-alerts")
def viral_alerts(region="KE"):
    new_viral = check_for_viral_videos(region=region)
    recent = get_recent_viral_alerts()
    return {"new": new_viral, "recent": recent}

@app.get("/localize")
def localize(video_id: str, region="KE", target="Kenya"):
    youtube = get_trending(region_code=region)
    video = next((v for v in youtube if v["id"] == video_id), None)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    package = generate_content_package(video, region=region)
    localized = localize_trend(video["title"], package.get("trend_explanation", ""), target_region=target)
    return {"localized": localized, "video": video}

@app.get("/cross-language")
def cross_language():
    return get_foreign_trends()

@app.get("/sentiment")
def sentiment(topic: str):
    return analyze_trend_sentiment(topic)

@app.get("/time-machine")
def time_machine(region="KE"):
    return get_historical_trends(region=region)

@app.post("/improve-script")
def improve_script_endpoint(request: ScriptRequest, region="KE"):
    improved = improve_script(request.script, niche=request.niche, target_region=region)
    return {"improved": improved}

@app.post("/repurpose")
def repurpose(request: RepurposeRequest):
    repurposed = repurpose_content(request.video_title, request.video_description, request.niche)
    return {"repurposed": repurposed}

@app.get("/hooks")
def hooks(niche: str = None):
    return {"hooks": get_best_hooks(niche=niche)}

@app.get("/generate-hooks")
def gen_hooks(topic: str, niche: str = "general"):
    hooks = generate_and_save_hooks(topic, niche=niche)
    return {"hooks": hooks}

@app.get("/search-intent")
def search_intent(topic: str):
    return analyze_search_intent(topic)

@app.get("/competitors")
def competitors():
    return {"channels": get_competitor_channels(), "data": get_all_competitor_data()}

@app.post("/competitors/add")
def add_competitor(channel: ChannelRequest):
    channels = add_competitor_channel(channel.dict())
    return {"channels": channels}

@app.delete("/competitors/{channel_id}")
def remove_competitor(channel_id: str):
    channels = remove_competitor_channel(channel_id)
    return {"channels": channels}

@app.get("/competitors/search")
def competitor_search(q: str):
    return {"results": search_channel(q)}

@app.get("/predict")
def predict(region="KE"):
    google = get_google_trends(region=region)
    predictions = predict_upcoming_trends(google, region=region)
    return {"predictions": predictions}

@app.post("/growth-simulator")
def growth_sim(request: GrowthRequest, region="KE"):
    simulation = simulate_growth(
        request.subscribers, request.avg_views,
        request.posts_per_week, request.niche, region
    )
    return {"simulation": simulation}

@app.get("/niches")
def niches(region="KE"):
    return {"niches": find_best_niches(region=region)}

@app.get("/monetization")
def monetization(region="KE"):
    google = get_google_trends(region=region)
    insights = get_monetization_insights(google, region=region)
    return {"insights": insights}

@app.post("/collab-finder")
def collab(request: CollabRequest, region="KE"):
    collabs = find_collab_opportunities(request.niche, request.subscribers, region)
    return {"collabs": collabs}

@app.get("/lifecycle")
def lifecycle(topic: str, velocity: int = 0, views: int = 0):
    return analyze_trend_lifecycle(topic, velocity, views)

@app.get("/health")
def health():
    return get_full_health_report()

@app.get("/notify")
def notify(category="0", region="KE"):
    result = fetch_and_notify(region=region, category=category)
    return {"status": "Notification sent!", "summary": result}

@app.get("/refresh")
def refresh():
    clear_cache()
    return {"status": "Cache cleared!"}