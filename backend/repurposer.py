import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def repurpose_content(video_title, video_description="", niche="general"):
    prompt = f"""
You are a content repurposing expert. Take this YouTube video and turn it into multiple content pieces.

Video title: {video_title}
Description: {video_description}
Niche: {niche}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "shorts_angles": [
    {{"angle": "angle 1", "hook": "hook for this angle", "script": "30 second script"}},
    {{"angle": "angle 2", "hook": "hook for this angle", "script": "30 second script"}},
    {{"angle": "angle 3", "hook": "hook for this angle", "script": "30 second script"}}
  ],
  "twitter_thread": ["tweet 1", "tweet 2", "tweet 3", "tweet 4", "tweet 5"],
  "instagram_caption": "engaging Instagram caption with hashtags",
  "tiktok_description": "TikTok optimized description",
  "youtube_description": "full YouTube description with keywords",
  "blog_outline": ["heading 1", "heading 2", "heading 3"],
  "newsletter_blurb": "2-3 sentence newsletter mention"
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
        print(f"Repurposer error: {e}")
        return {"shorts_angles": [], "twitter_thread": [], "instagram_caption": ""}