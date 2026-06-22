import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

def check_youtube_api():
    try:
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet",
            "chart": "mostPopular",
            "maxResults": 1,
            "key": os.getenv("YOUTUBE_API_KEY")
        }
        start = time.time()
        response = requests.get(url, params=params, timeout=10)
        latency = round((time.time() - start) * 1000)
        if response.status_code == 200:
            return {"status": "healthy", "latency_ms": latency}
        elif response.status_code == 403:
            return {"status": "quota_exceeded", "latency_ms": latency}
        else:
            return {"status": "error", "code": response.status_code, "latency_ms": latency}
    except Exception as e:
        return {"status": "down", "error": str(e)}

def check_groq_api():
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        start = time.time()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5
        )
        latency = round((time.time() - start) * 1000)
        return {"status": "healthy", "latency_ms": latency}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def check_news_api():
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {"apiKey": os.getenv("NEWS_API_KEY"), "pageSize": 1, "language": "en"}
        start = time.time()
        response = requests.get(url, params=params, timeout=10)
        latency = round((time.time() - start) * 1000)
        if response.status_code == 200:
            return {"status": "healthy", "latency_ms": latency}
        else:
            return {"status": "error", "code": response.status_code, "latency_ms": latency}
    except Exception as e:
        return {"status": "down", "error": str(e)}

def check_ntfy():
    try:
        topic = os.getenv("NTFY_TOPIC", "test")
        start = time.time()
        response = requests.get(f"https://ntfy.sh/{topic}/json?poll=1", timeout=10)
        latency = round((time.time() - start) * 1000)
        if response.status_code in [200, 404]:
            return {"status": "healthy", "latency_ms": latency}
        return {"status": "error", "latency_ms": latency}
    except Exception as e:
        return {"status": "down", "error": str(e)}

def get_full_health_report():
    return {
        "youtube": check_youtube_api(),
        "groq": check_groq_api(),
        "news": check_news_api(),
        "ntfy": check_ntfy(),
        "checked_at": time.time()
    }