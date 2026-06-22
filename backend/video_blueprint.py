import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_video_blueprint(video, content_package):
    title = video.get("title", "")
    script = content_package.get("script", "")
    sentiment = content_package.get("sentiment", "")
    hook = content_package.get("hook", "")

    prompt = f"""
You are a professional YouTube Shorts video director. Create an extremely detailed video blueprint.

Trend: {title}
Sentiment: {sentiment}
Hook: {hook}
Script: {script}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "video_style": "talking head/text only/screen recording/slideshow/voiceover",
  "total_duration": "exact seconds",
  "storyboard": [
    {{
      "timestamp": "0:00-0:03",
      "visual": "exactly what viewer sees",
      "audio": "exactly what they hear",
      "text_overlay": "any text on screen",
      "action": "what you do"
    }}
  ],
  "broll_needed": [
    {{
      "description": "what footage to find",
      "free_source": "Pexels/Pixabay/YouTube",
      "search_term": "exact search term to find it"
    }}
  ],
  "capcut_template": "which CapCut template style to use",
  "text_overlays": [
    {{
      "timestamp": "when to show",
      "text": "exact text",
      "style": "bold white/subtitle/title card",
      "duration": "how long to show"
    }}
  ],
  "transitions": ["transition between scene 1-2", "transition between scene 2-3"],
  "music_timing": "when music starts, drops, ends",
  "color_grade": "exact filter name in CapCut",
  "final_checklist": ["check 1", "check 2", "check 3", "check 4", "check 5"],
  "stock_footage_links": [
    {{"description": "what it is", "url": "https://www.pexels.com/search/relevant-term/"}}
  ]
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
        print(f"Video blueprint error: {e}")
        return {"storyboard": [], "broll_needed": [], "text_overlays": []}