import io
import os
import requests
import subprocess
import tempfile
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def fetch_pexels_images(query, count=5):
    try:
        headers = {"Authorization": PEXELS_API_KEY} if PEXELS_API_KEY else {}
        url = "https://api.pexels.com/v1/search"
        params = {"query": query, "per_page": count, "orientation": "portrait"}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        images = []
        for photo in data.get("photos", []):
            img_url = photo["src"]["portrait"]
            img_response = requests.get(img_url, timeout=15)
            if img_response.status_code == 200:
                images.append(img_response.content)
        return images
    except Exception as e:
        print(f"Pexels error: {e}")
        return []

def generate_voiceover(script, output_path):
    try:
        import edge_tts
        import asyncio

        clean_script = script.replace("[PAUSE]", "").replace("\n", " ").strip()

        async def generate():
            communicate = edge_tts.Communicate(clean_script, "en-US-AriaNeural")
            await communicate.save(output_path)

        asyncio.run(generate())
        return True
    except Exception as e:
        print(f"TTS error: {e}")
        return False

def generate_video(trend_title, script, search_query=None):
    try:
        from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
        from PIL import Image
        import numpy as np

        work_dir = tempfile.mkdtemp()
        query = search_query or trend_title

        print(f"Fetching images for: {query}")
        images = fetch_pexels_images(query, count=6)

        if not images:
            images = fetch_pexels_images("trending viral social media", count=6)

        if not images:
            return None, "Could not fetch images"

        image_paths = []
        for i, img_data in enumerate(images):
            img_path = os.path.join(work_dir, f"image_{i}.jpg")
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((1080, 1920), Image.LANCZOS)
            img.save(img_path)
            image_paths.append(img_path)

        print("Generating voiceover...")
        audio_path = os.path.join(work_dir, "voiceover.mp3")
        if not generate_voiceover(script, audio_path):
            return None, "Could not generate voiceover"

        print("Assembling video...")
        audio = AudioFileClip(audio_path)
        total_duration = audio.duration
        duration_per_image = total_duration / len(image_paths)

        clips = []
        for img_path in image_paths:
            clip = ImageClip(img_path, duration=duration_per_image)
            clips.append(clip)

        video = concatenate_videoclips(clips, method="compose")
        video = video.set_audio(audio)

        output_path = os.path.join(work_dir, "output.mp4")
        video.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None
        )

        print("Video generated successfully!")
        return output_path, None

    except Exception as e:
        print(f"Video generation error: {e}")
        return None, str(e)