import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_multiplatform_content(video_title, script, hashtags, region="KE"):
    prompt = f"""
You are a multi-platform content strategist. Take this YouTube Shorts content and optimize it for every platform.

Video title: {video_title}
Script: {script}
Hashtags: {", ".join(hashtags) if hashtags else ""}
Region: {region}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "youtube": {{
    "title": "optimized YouTube title",
    "description": "full YouTube description with keywords",
    "hashtags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
    "tags": ["tag1", "tag2", "tag3"],
    "thumbnail_text": "text to put on thumbnail"
  }},
  "tiktok": {{
    "caption": "TikTok caption under 150 chars",
    "hashtags": ["tag1", "tag2", "tag3"],
    "sound_suggestion": "trending sound to use",
    "best_time": "best time to post on TikTok"
  }},
  "instagram": {{
    "caption": "Instagram Reels caption",
    "hashtags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
    "story_text": "text for Instagram story promoting the reel",
    "best_time": "best time to post on Instagram"
  }},
  "twitter": {{
    "tweet": "tweet promoting the video under 280 chars",
    "thread": ["tweet 1", "tweet 2", "tweet 3"],
    "best_time": "best time to post on Twitter"
  }},
  "best_platform_today": "which platform to prioritize today and why"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Multiplatform error: {e}")
        return {}