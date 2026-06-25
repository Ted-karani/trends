import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def translate_trend(trend_title, region="KE"):
    prompt = f"""
You are a trend explainer. Someone just saw "{trend_title}" trending and has no idea what it is.

Explain it simply and completely. Return ONLY a JSON object, no markdown, no backticks:

{{
  "what_it_is": "simple one sentence explanation",
  "full_explanation": "2-3 paragraph explanation a complete beginner would understand",
  "origin": "where and how it started",
  "why_viral": "exactly why people are sharing this",
  "key_people": ["person/account involved 1", "person 2"],
  "timeline": "when it started and how it spread",
  "cultural_context": "any cultural background needed to understand it",
  "controversy": "any controversy around it or null",
  "how_to_explain_in_video": "how a creator in {region} should explain this to their audience",
  "simple_summary": "explain it like I'm 10 years old in one sentence"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=800
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Trend translator error: {e}")
        return {"what_it_is": "", "full_explanation": "", "simple_summary": ""}