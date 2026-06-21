import requests
import os
from dotenv import load_dotenv

load_dotenv()

NTFY_TOPIC = os.getenv("NTFY_TOPIC")

def send_notification(title, message):
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode("utf-8"),
            headers={
                "Title": title,
                "Priority": "default",
                "Content-Type": "text/plain; charset=utf-8"
            },
            timeout=10
        )
        print("Notification sent!")
    except Exception as e:
        print(f"Notification error: {e}")

def notify_trending(summary):
    if not summary:
        return
    send_notification("Trending Now", summary)