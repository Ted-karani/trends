import os
from groq import Groq
from dotenv import load_dotenv
from storage import get_trend_history

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_personalized_lessons(channel_name="funny_needs_help", region="KE"):
    history = get_trend_history()
    history_text = "\n".join([
        f"- {h['title']} | views: {h.get('views', 0):,}"
        for h in history[-20:]
    ]) if history else "No history yet"

    prompt = f"""
You are a YouTube Shorts coach and mentor. Give personalized lessons to this creator.

Creator: {channel_name}
Region: {region}
Content history tracked:
{history_text}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "overall_assessment": "overall assessment of the creator's potential",
  "skill_levels": {{
    "trend_detection": "Beginner/Intermediate/Advanced",
    "content_strategy": "Beginner/Intermediate/Advanced",
    "hook_writing": "Beginner/Intermediate/Advanced",
    "consistency": "Beginner/Intermediate/Advanced"
  }},
  "lessons": [
    {{
      "lesson_number": 1,
      "title": "lesson title",
      "skill": "what skill this builds",
      "why_important": "why this matters for growth",
      "lesson_content": "the actual lesson explanation",
      "exercise": "practical exercise to do today",
      "success_criteria": "how to know you've mastered this"
    }},
    {{
      "lesson_number": 2,
      "title": "lesson title",
      "skill": "what skill this builds",
      "why_important": "why this matters",
      "lesson_content": "the lesson",
      "exercise": "practical exercise",
      "success_criteria": "mastery criteria"
    }},
    {{
      "lesson_number": 3,
      "title": "lesson title",
      "skill": "what skill this builds",
      "why_important": "why this matters",
      "lesson_content": "the lesson",
      "exercise": "practical exercise",
      "success_criteria": "mastery criteria"
    }}
  ],
  "this_weeks_focus": "single most important thing to focus on this week",
  "motivation": "personalized motivational message"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1200
        )
        import json
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Academy error: {e}")
        return {"lessons": [], "motivation": "Keep going!"}