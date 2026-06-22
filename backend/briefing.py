import os
from groq import Groq
from dotenv import load_dotenv
from opportunity import get_opportunities
from cache import get_cache, set_cache

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_morning_briefing(region="KE"):
    cache_key = f"briefing_{region}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    try:
        opportunities = get_opportunities(region=region)
        all_opps = opportunities.get("all", [])[:10]
        signals = opportunities.get("signals", [])[:5]

        opp_text = "\n".join([
            f"- {o['title']} | Score: {o['opportunity_score']} | Urgency: {o['urgency']} | Views: {o['views']:,}"
            for o in all_opps
        ])

        signal_text = "\n".join([
            f"- {s['term']} | {s['strength']} | Platforms: {', '.join(s['platforms'])}"
            for s in signals
        ])

        prompt = f"""
You are a personal content strategist giving a creator their morning briefing.

Today's top opportunities:
{opp_text}

Cross platform signals:
{signal_text}

Give them a punchy morning briefing. Return ONLY a JSON object, no markdown, no backticks:

{{
  "greeting": "energetic good morning message mentioning what kind of day it is for content",
  "top_3": [
    {{
      "rank": 1,
      "topic": "topic name",
      "why": "one sentence why this is the best opportunity today",
      "urgency": "Post Now/Post Today/Post This Week",
      "predicted_views": "realistic view estimate"
    }},
    {{
      "rank": 2,
      "topic": "topic name",
      "why": "one sentence why",
      "urgency": "urgency level",
      "predicted_views": "view estimate"
    }},
    {{
      "rank": 3,
      "topic": "topic name",
      "why": "one sentence why",
      "urgency": "urgency level",
      "predicted_views": "view estimate"
    }}
  ],
  "super_trend": "the single biggest trend right now in one punchy sentence or null",
  "avoid_today": "any trend to avoid and why or null",
  "motivation": "short motivational message to get them creating"
}}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=800
        )

        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)
        set_cache(cache_key, result)
        return result

    except Exception as e:
        print(f"Briefing error: {e}")
        return {
            "greeting": "Good morning! Let's check what's trending today.",
            "top_3": [],
            "super_trend": None,
            "avoid_today": None,
            "motivation": "Every Short you post is a chance to go viral. Let's go!"
        }