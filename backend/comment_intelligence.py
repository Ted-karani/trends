import os
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_video_comments(video_id, max_results=50):
    try:
        url = "https://www.googleapis.com/youtube/v3/commentThreads"
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": max_results,
            "order": "relevance",
            "key": API_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        comments = []
        for item in data.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "text": comment["textDisplay"],
                "likes": comment["likeCount"],
                "author": comment["authorDisplayName"]
            })
        return comments
    except Exception as e:
        print(f"Comments error: {e}")
        return []

def analyze_comments(video_id, video_title=""):
    comments = get_video_comments(video_id)
    if not comments:
        return {"error": "No comments found"}

    comments_text = "\n".join([
        f"- [{c['likes']} likes] {c['text']}"
        for c in comments[:30]
    ])

    prompt = f"""
You are a YouTube audience analyst. Analyze these comments from a trending video.

Video: {video_title}
Comments:
{comments_text}

Return ONLY a JSON object, no markdown, no backticks:

{{
  "audience_wants": ["what they want more of 1", "what they want 2", "what they want 3"],
  "audience_complaints": ["what they dont like 1", "complaint 2"],
  "questions_asked": ["question people are asking 1", "question 2", "question 3"],
  "viral_phrases": ["phrase being repeated 1", "phrase 2"],
  "sentiment": "overall positive/negative/mixed",
  "content_opportunities": ["content idea from comments 1", "idea 2", "idea 3"],
  "follow_up_video_ideas": ["follow up idea 1", "follow up idea 2"],
  "audience_profile": "description of who is watching this",
  "engagement_triggers": ["what triggered most engagement 1", "trigger 2"]
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
        print(f"Comment analysis error: {e}")
        return {"error": str(e)}