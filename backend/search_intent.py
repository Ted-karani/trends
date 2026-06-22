from search_volume import get_autocomplete_suggestions
from groq import Groq
import os
from dotenv import load_dotenv
from cache import get_cache, set_cache

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_search_intent(trend_title):
    cache_key = f"intent_{trend_title[:30]}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    suggestions = get_autocomplete_suggestions(trend_title)

    prompt = f"""
Analyze what people are searching for around this trend: "{trend_title}"
Related searches: {", ".join(suggestions)}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "primary_intent": "what most people want to know",
  "questions_people_ask": ["question 1", "question 2", "question 3", "question 4", "question 5"],
  "content_gaps": ["topic not being covered 1", "topic not being covered 2"],
  "best_content_format": "what format answers this intent best",
  "seo_keywords": ["keyword 1", "keyword 2", "keyword 3"],
  "search_volume_estimate": "Low/Medium/High/Very High",
  "competition_level": "Low/Medium/High",
  "opportunity_score": a number from 1-100,
  "recommended_title": "SEO optimized title that matches search intent"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=600
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)
        set_cache(cache_key, result)
        return result
    except Exception as e:
        print(f"Search intent error: {e}")
        return {"primary_intent": "", "questions_people_ask": [], "seo_keywords": []}