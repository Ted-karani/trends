import os
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_video_details(video_id):
    try:
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics,contentDetails",
            "id": video_id,
            "key": API_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        items = data.get("items", [])
        if not items:
            return None
        item = items[0]
        snippet = item["snippet"]
        stats = item.get("statistics", {})
        duration = item.get("contentDetails", {}).get("duration", "")
        return {
            "title": snippet["title"],
            "description": snippet.get("description", "")[:500],
            "channel": snippet["channelTitle"],
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "duration": duration,
            "thumbnail": snippet["thumbnails"]["high"]["url"]
        }
    except Exception as e:
        print(f"Video details error: {e}")
        return None

def get_timestamped_comments(video_id, max_results=100):
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

        timestamped = []
        all_comments = []

        for item in data.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]
            text = comment["textDisplay"]
            likes = comment["likeCount"]

            import re
            timestamps = re.findall(r'\b(\d{1,2}:\d{2}(?::\d{2})?)\b', text)

            all_comments.append({
                "text": text[:200],
                "likes": likes,
                "has_timestamp": len(timestamps) > 0,
                "timestamps": timestamps
            })

            if timestamps:
                timestamped.append({
                    "text": text[:200],
                    "likes": likes,
                    "timestamps": timestamps
                })

        timestamped_sorted = sorted(
            timestamped,
            key=lambda x: x["likes"],
            reverse=True
        )

        return {
            "timestamped": timestamped_sorted[:20],
            "all": all_comments[:30]
        }

    except Exception as e:
        print(f"Comments error: {e}")
        return {"timestamped": [], "all": []}

def generate_clip_guide(video_id):
    video = get_video_details(video_id)
    if not video:
        return {"error": "Video not found"}

    comments_data = get_timestamped_comments(video_id)
    timestamped = comments_data["timestamped"]
    all_comments = comments_data["all"]

    timestamps_text = "\n".join([
        f"- [{', '.join(c['timestamps'])}] ({c['likes']} likes): {c['text'][:100]}"
        for c in timestamped[:15]
    ]) if timestamped else "No timestamp comments found"

    comments_text = "\n".join([
        f"- ({c['likes']} likes): {c['text'][:100]}"
        for c in all_comments[:15]
    ])

    prompt = f"""
You are a viral clip finder and YouTube Shorts strategist.

Video: {video['title']}
Channel: {video['channel']}
Views: {video['views']:,}
Likes: {video['likes']:,}
Duration: {video['duration']}
Description: {video['description']}

Comments mentioning timestamps:
{timestamps_text}

Top comments (by likes):
{comments_text}

Based on this data, identify the best moments to clip for YouTube Shorts.
Return ONLY a JSON object, no markdown, no backticks:

{{
  "video_type": "funny/reaction/educational/sports/music/news",
  "best_clips": [
    {{
      "clip_number": 1,
      "timestamp_start": "exact timestamp like 0:47",
      "timestamp_end": "exact timestamp like 1:15",
      "duration_seconds": 28,
      "why_viral": "why this moment is going viral based on comments",
      "clip_title": "title for this Short",
      "caption": "caption to use when posting",
      "hook": "how to introduce this clip in first 2 seconds",
      "clip_type": "funny/shocking/informative/emotional/highlight",
      "viral_potential": "High/Medium/Low",
      "comment_evidence": "what comments say about this moment"
    }}
  ],
  "posting_order": "which clip to post first and why",
  "best_clip_index": 0,
  "editing_tips": ["tip 1 for editing these clips", "tip 2", "tip 3"],
  "capcut_steps": [
    "Step 1: Open CapCut",
    "Step 2: Import the video",
    "Step 3: specific editing step",
    "Step 4: specific editing step",
    "Step 5: Export and post"
  ],
  "hashtags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "overall_assessment": "overall assessment of this video's clip potential"
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
        result = json.loads(text)
        result["video"] = video
        result["timestamp_comments"] = timestamped[:5]
        return result
    except Exception as e:
        print(f"Clip guide error: {e}")
        return {"error": str(e), "video": video}