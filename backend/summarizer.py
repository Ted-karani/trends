import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_trends(youtube_videos, google_trends, reddit_posts, news_articles=None):
    youtube_titles = "\n".join([
        f"- {v['title']} by {v['channel']} ({v.get('views', 0):,} views, velocity: {v.get('velocity', 0):,}/hr)"
        for v in youtube_videos[:10]
    ])
    google_list = "\n".join([f"- {t}" for t in google_trends[:10]])
    news_list = "\n".join([
        f"- [{a.get('source', '')}] {a.get('title', '')}"
        for a in (news_articles or [])[:5]
    ])

    prompt = f"""
You are an internet culture analyst who knows everything about memes, viral trends, music, sports, and social media.

Look at this data from YouTube, Google Trends and News. Tell me exactly what is popping right now.

Rules:
- Call out specific meme names if you spot them
- Mention specific artists, players, teams, or people by name
- Identify viral phrases or sounds
- Group related trends together
- Write like a cool friend texting, not a news report
- Use emojis
- Be specific not vague
- Keep under 250 words

YOUTUBE TRENDING:
{youtube_titles}

GOOGLE TRENDS:
{google_list}

NEWS:
{news_list}

What's actually popping right now?
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq error: {e}")
        return "Could not generate summary right now. Check back soon!"