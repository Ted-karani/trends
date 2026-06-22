from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def simulate_growth(current_subscribers, current_views_avg, posting_frequency, niche, region="KE"):
    prompt = f"""
You are a YouTube growth analyst. Simulate growth scenarios for this creator.

Current stats:
- Subscribers: {current_subscribers}
- Average views per video: {current_views_avg}
- Posting frequency: {posting_frequency} videos per week
- Niche: {niche}
- Region: {region}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "current_analysis": "assessment of current channel health",
  "scenarios": [
    {{
      "name": "Conservative",
      "frequency": "{posting_frequency} videos/week",
      "30_days": {{"subscribers": 0, "avg_views": 0}},
      "90_days": {{"subscribers": 0, "avg_views": 0}},
      "6_months": {{"subscribers": 0, "avg_views": 0}}
    }},
    {{
      "name": "Aggressive",
      "frequency": "2x current frequency",
      "30_days": {{"subscribers": 0, "avg_views": 0}},
      "90_days": {{"subscribers": 0, "avg_views": 0}},
      "6_months": {{"subscribers": 0, "avg_views": 0}}
    }},
    {{
      "name": "Viral Scenario",
      "frequency": "1 video hits 1M+ views",
      "30_days": {{"subscribers": 0, "avg_views": 0}},
      "90_days": {{"subscribers": 0, "avg_views": 0}},
      "6_months": {{"subscribers": 0, "avg_views": 0}}
    }}
  ],
  "key_milestones": [
    {{"milestone": "500 subscribers", "estimated_when": "timeframe", "what_changes": "what happens at this milestone"}},
    {{"milestone": "1000 subscribers", "estimated_when": "timeframe", "what_changes": "YouTube Partner Program eligible"}},
    {{"milestone": "10000 subscribers", "estimated_when": "timeframe", "what_changes": "brand deal territory"}}
  ],
  "biggest_growth_lever": "the single most impactful thing to do right now",
  "warning": "biggest risk to growth or null"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=1000
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Growth simulator error: {e}")
        return {"scenarios": [], "key_milestones": []}