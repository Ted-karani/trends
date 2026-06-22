from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_monetization_insights(trending_topics, niche="general", region="KE"):
    topics_text = "\n".join([f"- {t}" for t in trending_topics[:10]])

    prompt = f"""
You are a YouTube monetization expert. Based on these trending topics, identify monetization opportunities.

Trending topics:
{topics_text}

Creator niche: {niche}
Region: {region}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "brand_opportunities": [
    {{
      "brand_category": "type of brand that would pay for this",
      "trending_topic": "which trend connects",
      "pitch_angle": "how to pitch yourself",
      "estimated_deal_value": "realistic deal value range"
    }}
  ],
  "affiliate_opportunities": [
    {{
      "product_category": "what to promote",
      "relevant_trend": "which trend connects",
      "platforms": ["Amazon", "etc"]
    }}
  ],
  "adsense_potential": "estimated RPM range for this niche and region",
  "best_monetization_path": "the fastest path to making money given current trends",
  "trending_sponsor_categories": ["category 1", "category 2", "category 3"]
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
        print(f"Monetization error: {e}")
        return {"brand_opportunities": [], "affiliate_opportunities": []}