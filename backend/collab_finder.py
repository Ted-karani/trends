from competitor import search_channel, get_channel_recent_videos
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def find_collab_opportunities(your_niche, your_subscriber_count, region="KE"):
    search_queries = [
        f"{your_niche} creator {region}",
        f"YouTube Shorts {your_niche}",
        f"trending {your_niche} channel"
    ]

    potential_creators = []
    for query in search_queries:
        channels = search_channel(query)
        potential_creators.extend(channels[:2])

    if not potential_creators:
        return []

    creators_text = "\n".join([
        f"- {c['name']}: {c['description']}"
        for c in potential_creators[:6]
    ])

    prompt = f"""
You are a YouTube collab strategist. Find the best collab opportunities.

Your channel niche: {your_niche}
Your subscribers: {your_subscriber_count}
Region: {region}

Potential creators found:
{creators_text}

Return ONLY a JSON array, no markdown, no backticks:

[
  {{
    "creator_name": "name",
    "why_good_fit": "why this collab makes sense",
    "collab_idea": "specific collab video idea",
    "pitch_message": "ready to send DM pitch",
    "expected_benefit": "what you both gain"
  }}
]
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
        print(f"Collab finder error: {e}")
        return []