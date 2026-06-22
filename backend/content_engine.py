import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_content_package(video, region="KE"):
    title = video.get("title", "")
    channel = video.get("channel", "")
    views = video.get("views", 0)
    urgency = video.get("urgency", "Watch")
    reasons = video.get("reasons", [])

    prompt = f"""
You are an expert YouTube Shorts content strategist who knows exactly what makes videos go viral.

A video is trending:
Title: {title}
Channel: {channel}
Views: {views:,}
Urgency: {urgency}
Why it's trending: {", ".join(reasons)}
Creator region: {region}

Generate a complete content package for making a YouTube Short about this trend. Return ONLY a JSON object with exactly these fields, no markdown, no backticks:

{{
  "trend_explanation": "2-3 sentences explaining what this trend is about and why it's going viral",
  "sentiment": "the overall mood/tone of this trend (hype/funny/emotional/controversial/inspiring)",
  "trend_origin": "where did this trend start and how did it spread",
  "difficulty": "Easy/Medium/Hard (based on how many creators are likely already covering this)",
  "expiry": "how long this trend will last (24 hours/2-3 days/1 week/evergreen)",
  "script": "a complete ready-to-record 35-40 second YouTube Shorts script with [PAUSE] markers",
  "hook": "the perfect first 2 seconds - make it impossible to scroll past",
  "hook_alternatives": ["alternative hook 1", "alternative hook 2", "alternative hook 3"],
  "title_options": ["SEO optimized title 1", "clickbait title 2", "question title 3"],
  "hashtags": ["hashtag1", "hashtag2", "hashtag3", "hashtag4", "hashtag5"],
  "thumbnail_concept": "detailed description of what the thumbnail should look like",
  "best_time_to_post": "specific time recommendation with reason",
  "predicted_views": "realistic view range estimate for a small channel",
  "series_potential": "could this become a series? explain briefly",
  "similar_angles": ["unique angle 1 nobody is covering", "unique angle 2", "unique angle 3"],
  "comment_prompt": "a question to pin in comments to drive engagement",
  "caption_style": "what text style to use in the Short (bold white/subtitles/minimal/etc)",
  "controversy_warning": "any potential controversy to be aware of or null",
  "evergreen_score": "1-10 how long this content will get views after posting"
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Content engine error: {e}")
        return {
            "trend_explanation": "Could not generate content package",
            "script": "",
            "hook": "",
            "hook_alternatives": [],
            "title_options": [],
            "hashtags": [],
            "thumbnail_concept": "",
            "best_time_to_post": "",
            "predicted_views": "",
            "sentiment": "",
            "trend_origin": "",
            "difficulty": "",
            "expiry": "",
            "series_potential": "",
            "similar_angles": [],
            "comment_prompt": "",
            "caption_style": "",
            "controversy_warning": None,
            "evergreen_score": 0
        }