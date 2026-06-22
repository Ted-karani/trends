from groq import Groq
import os
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_trend_lifecycle(trend_title, current_velocity=0, views=0):
    cache_key = f"lifecycle_{trend_title[:30]}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    prompt = f"""
Analyze the lifecycle of this trend: "{trend_title}"
Current velocity: {current_velocity:,} views/hour
Total views: {views:,}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "current_phase": "emerging/rising/peak/declining/dead",
  "phase_percentage": a number 0-100 showing how far through this phase,
  "hours_until_peak": estimated hours until this peaks or null if already peaked,
  "hours_until_dead": estimated hours until this trend is over,
  "post_window": "how many hours left to post and still get views",
  "urgency": "Post Now/Post Soon/Already Late/Too Late",
  "lifecycle_summary": "one sentence summary of where this trend is",
  "similar_past_trends": ["trend that followed same pattern 1", "trend 2"],
  "peak_view_estimate": "estimated total views at peak"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=400
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)
        set_cache(cache_key, result)
        return result
    except Exception as e:
        print(f"Lifecycle error: {e}")
        return {
            "current_phase": "unknown",
            "urgency": "Post Soon",
            "post_window": "Unknown",
            "lifecycle_summary": "Unable to analyze lifecycle"
        }