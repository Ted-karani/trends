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
        work_dir = tempfile.mkdtemp()
        query = search_query or trend_title

        print(f"Fetching images for: {query}")
        images = fetch_pexels_images(query, count=6)

        if not images:
            print("No images found, using fallback")
            images = fetch_pexels_images("trending viral social media", count=6)

        image_paths = []
        for i, img_data in enumerate(images):
            img_path = os.path.join(work_dir, f"image_{i}.jpg")
            with open(img_path, "wb") as f:
                f.write(img_data)
            image_paths.append(img_path)

        if not image_paths:
            return None, "Could not fetch images"

        print("Generating voiceover...")
        audio_path = os.path.join(work_dir, "voiceover.mp3")
        if not generate_voiceover(script, audio_path):
            return None, "Could not generate voiceover"

        print("Assembling video...")
        output_path = os.path.join(work_dir, "output.mp4")

        duration_per_image = max(3, 45 // len(image_paths))

        filter_parts = []
        input_args = []

        for i, img_path in enumerate(image_paths):
            input_args.extend(["-loop", "1", "-t", str(duration_per_image), "-i", img_path])

        input_args.extend(["-i", audio_path])

        audio_index = len(image_paths)

        for i in range(len(image_paths)):
            filter_parts.append(
                f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,"
                f"crop=1080:1920,setsar=1,fps=30[v{i}]"
            )

        concat_inputs = "".join([f"[v{i}]" for i in range(len(image_paths))])
        filter_parts.append(f"{concat_inputs}concat=n={len(image_paths)}:v=1:a=0[outv]")

        filter_complex = ";".join(filter_parts)

        cmd = [
            "ffmpeg", "-y",
            *input_args,
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", f"{audio_index}:a",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            "-movflags", "+faststart",
            output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return None, "Video assembly failed"

        print("Video generated successfully!")
        return output_path, None

    except Exception as e:
        print(f"Video generation error: {e}")
        return None, str(e)