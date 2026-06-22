import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def localize_trend(trend_title, trend_explanation, target_region="Kenya"):
    prompt = f"""
You are a content strategist who specializes in localizing global trends for African audiences.

Global trend: {trend_title}
What it is: {trend_explanation}
Target region: {target_region}

Localize this trend for the target region. Return ONLY a JSON object, no markdown, no backticks:

{{
  "local_angle": "how to present this trend specifically for {target_region} audience",
  "local_context": "any local events, culture, or references that connect to this trend",
  "local_hook": "a hook written specifically for {target_region} viewers",
  "local_script": "a 30 second script rewritten with local flavor and references",
  "local_hashtags": ["local hashtag 1", "local hashtag 2", "local hashtag 3"],
  "local_sound": "what type of music or sound would resonate with this audience",
  "posting_tip": "specific tip for posting this content in {target_region}",
  "avoid": "anything to avoid that might not land well locally"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Localization error: {e}")
        return {"local_angle": "Could not localize", "local_hook": "", "local_script": ""}