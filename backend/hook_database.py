from storage import save_hook, get_hooks
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_and_save_hooks(trend_title, niche="general", score=0):
    prompt = f"""
Generate 5 different viral YouTube Shorts hooks for this trend: "{trend_title}"
Niche: {niche}

Return ONLY a JSON array, no markdown, no backticks:
[
  {{
    "hook": "the hook text",
    "type": "question/shock/controversial/relatable/educational",
    "why_it_works": "brief explanation"
  }}
]
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=600
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        hooks = json.loads(text)

        for hook in hooks:
            save_hook({
                "hook": hook["hook"],
                "type": hook["type"],
                "why_it_works": hook["why_it_works"],
                "trend": trend_title,
                "niche": niche,
                "score": score
            })

        return hooks
    except Exception as e:
        print(f"Hook database error: {e}")
        return []

def get_best_hooks(niche=None, limit=20):
    return get_hooks(niche=niche)[:limit]