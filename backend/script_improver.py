import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def improve_script(original_script, niche="general", target_region="Kenya"):
    prompt = f"""
You are an expert YouTube Shorts script editor who has helped creators get millions of views.

Original script:
{original_script}

Niche: {niche}
Target audience: {target_region}

Rewrite and improve this script. Return ONLY a JSON object, no markdown, no backticks:

{{
  "improved_script": "the fully rewritten improved script",
  "new_hook": "improved opening hook",
  "changes_made": ["change 1", "change 2", "change 3"],
  "why_better": "explanation of why the new version will perform better",
  "pacing_notes": "where to speed up, slow down, pause",
  "energy_level": "what energy to bring when recording this",
  "estimated_duration": "how long this script takes to deliver",
  "retention_score": "predicted retention improvement from 1-10"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Script improver error: {e}")
        return {"improved_script": original_script, "changes_made": [], "why_better": ""}