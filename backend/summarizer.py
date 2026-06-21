import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_trends(youtube_videos, google_trends, reddit_posts):
    youtube_titles = "\n".join([f"- {v['title']} by {v['channel']} ({v['views']:,} views)" for v in youtube_videos[:10]])
    google_list = "\n".join([f"- {t}" for t in google_trends[:10]])
    reddit_list = "\n".join([f"- [r/{p['subreddit']}] {p['title']} ({p['upvotes']:,} upvotes)" for p in reddit_posts[:10]])

    prompt = f"""
You are an internet culture analyst who knows everything about memes, viral trends, music, sports, and social media.

Look at the data below from YouTube, Google Trends, and Reddit. Your job is to tell me exactly what is popping right now in internet culture in a fun, specific, and punchy way.

Rules:
- Call out specific meme names if you spot them
- Mention specific artists, players, teams, or people by name
- Identify viral phrases or sounds if you see them
- Group related trends together (e.g. if multiple sources mention the same thing)
- Write like a cool friend texting you, not a news report
- Use emojis throughout
- Be specific, not vague — say "Bellingham edits are everywhere" not "football content is trending"
- Keep it under 250 words

YOUTUBE TRENDING:
{youtube_titles}

GOOGLE TRENDS:
{google_list}

REDDIT HOT POSTS:
{reddit_list}

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