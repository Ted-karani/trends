import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_best_format(trend_title, trend_data):
    prompt = f"""
You are a YouTube format strategist. Decide whether this trend is better as a Short or long form video.

Trend: {trend_title}
Data: {trend_data}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "recommended_format": "Short/Long Form/Both",
  "confidence": "High/Medium/Low",
  "short_pros": ["why Short works 1", "why Short works 2"],
  "short_cons": ["why Short might not work 1"],
  "long_form_pros": ["why long form works 1", "why long form works 2"],
  "long_form_cons": ["why long form might not work 1"],
  "ideal_short_length": "ideal Short duration in seconds",
  "ideal_long_length": "ideal long form duration in minutes",
  "short_angle": "best angle if doing a Short",
  "long_form_angle": "best angle if doing long form",
  "monetization_potential": {{
    "short": "monetization potential for Short",
    "long_form": "monetization potential for long form"
  }},
  "final_recommendation": "clear final recommendation with reasoning"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=700
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Format analyzer error: {e}")
        return {"recommended_format": "Short", "final_recommendation": ""}