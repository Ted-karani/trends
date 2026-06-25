import os
from groq import Groq
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_personal_brand(channel_name, niche, region="KE", style="energetic"):
    cache_key = f"brand_{channel_name}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    prompt = f"""
You are a personal brand strategist for YouTube creators.

Channel: {channel_name}
Niche: {niche}
Region: {region}
Style preference: {style}

Build a complete personal brand guide. Return ONLY a JSON object, no markdown, no backticks:

{{
  "brand_identity": {{
    "tagline": "memorable channel tagline",
    "brand_voice": "description of how to speak and write",
    "personality_traits": ["trait 1", "trait 2", "trait 3"],
    "catchphrase": "signature phrase to use in every video"
  }},
  "visual_identity": {{
    "color_palette": ["primary color", "secondary color", "accent color"],
    "font_style": "font style recommendation",
    "thumbnail_style": "consistent thumbnail style description",
    "logo_concept": "simple logo idea"
  }},
  "content_pillars": [
    {{"pillar": "content type 1", "percentage": "40%", "examples": ["example 1", "example 2"]}},
    {{"pillar": "content type 2", "percentage": "35%", "examples": ["example 1", "example 2"]}},
    {{"pillar": "content type 3", "percentage": "25%", "examples": ["example 1", "example 2"]}}
  ],
  "target_audience": {{
    "age_range": "age range",
    "interests": ["interest 1", "interest 2", "interest 3"],
    "pain_points": ["what they struggle with 1", "pain point 2"],
    "why_they_watch_you": "what unique value you provide"
  }},
  "competitive_advantage": "what makes this channel unique",
  "channels_to_study": ["similar successful channel 1", "channel 2"],
  "first_10_videos": ["video idea 1", "idea 2", "idea 3", "idea 4", "idea 5"]
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
        result = json.loads(text)
        set_cache(cache_key, result)
        return result
    except Exception as e:
        print(f"Brand builder error: {e}")
        return {}