import os
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_production_guide(video, content_package):
    title = video.get("title", "")
    sentiment = content_package.get("sentiment", "")
    script = content_package.get("script", "")
    caption_style = content_package.get("caption_style", "")

    prompt = f"""
You are an expert mobile video production coach for YouTube Shorts.

A creator needs to film a Short about: {title}
Tone/sentiment: {sentiment}
Script: {script}
Caption style: {caption_style}

Give them a complete step by step production guide. Return ONLY a JSON object, no markdown, no backticks:

{{
  "total_time_needed": "realistic time to film and edit this Short",
  "recommended_app": "best free mobile app for this type of Short with reason",
  "alternative_apps": ["app 2", "app 3"],
  "recommended_sound": "specific type of sound/music to use and why",
  "filming_steps": [
    {{"step": 1, "action": "what to do", "tip": "pro tip for this step"}},
    {{"step": 2, "action": "what to do", "tip": "pro tip for this step"}}
  ],
  "editing_steps": [
    {{"step": 1, "action": "what to do in the editor", "tip": "pro tip"}},
    {{"step": 2, "action": "what to do in the editor", "tip": "pro tip"}}
  ],
  "text_overlay": "exactly what text to add and when (with timestamps)",
  "transitions": "what transitions to use or avoid",
  "color_grade": "what filter or color tone works for this trend",
  "export_settings": "exact export settings for best quality",
  "upload_checklist": ["item 1 to check before posting", "item 2", "item 3"],
  "common_mistakes": ["mistake to avoid 1", "mistake to avoid 2"]
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1200
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Producer error: {e}")
        return {
            "total_time_needed": "30-45 minutes",
            "recommended_app": "CapCut",
            "alternative_apps": ["VN", "InShot"],
            "recommended_sound": "Use a trending sound from YouTube audio library",
            "filming_steps": [],
            "editing_steps": [],
            "text_overlay": "",
            "transitions": "",
            "color_grade": "",
            "export_settings": "1080x1920, 60fps",
            "upload_checklist": [],
            "common_mistakes": []
        }