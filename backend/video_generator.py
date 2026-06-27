import os
import io
import requests
import tempfile
import asyncio
import shutil
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def fetch_pexels_images(query, count=3):
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

        clean_script = script.replace("[PAUSE]", "").replace("\n", " ").strip()
        clean_script = clean_script[:400]

        async def generate():
            communicate = edge_tts.Communicate(clean_script, "en-US-AriaNeural")
            await communicate.save(output_path)

        asyncio.run(generate())
        return True
    except Exception as e:
        print(f"TTS error: {e}")
        return False

def create_text_overlay(img, text, position="bottom"):
    draw = ImageDraw.Draw(img)
    width, height = img.size

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
    except:
        font = ImageFont.load_default()

    words = text.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        test_line = " ".join(current_line)
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] > width - 80:
            current_line.pop()
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))

    lines = lines[:3]
    line_height = 55
    total_height = len(lines) * line_height + 40

    if position == "bottom":
        y_start = height - total_height - 80
    else:
        y_start = 80

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(
        [40, y_start - 10, width - 40, y_start + total_height],
        fill=(0, 0, 0, 160)
    )
    img_rgba = img.convert("RGBA")
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    final_draw = ImageDraw.Draw(img_rgba)

    for i, line in enumerate(lines):
        y = y_start + i * line_height + 10
        bbox = final_draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        final_draw.text((x + 2, y + 2), line, font=font, fill=(0, 0, 0, 255))
        final_draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))

    return img_rgba.convert("RGB")

def generate_video(trend_title, script, search_query=None):
    try:
        import subprocess
        work_dir = tempfile.mkdtemp()
        query = search_query or trend_title

        print(f"Fetching images for: {query}")
        images_data = fetch_pexels_images(query, count=3)

        if not images_data:
            images_data = fetch_pexels_images("trending viral", count=3)

        if not images_data:
            return None, "Could not fetch images"

        print("Generating voiceover...")
        audio_path = os.path.join(work_dir, "voiceover.mp3")
        if not generate_voiceover(script, audio_path):
            return None, "Could not generate voiceover"

        print("Processing images...")
        script_words = script.replace("[PAUSE]", "").split()
        words_per_image = max(1, len(script_words) // len(images_data))

        frame_paths = []
        for i, img_data in enumerate(images_data):
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((720, 1280), Image.LANCZOS)

            start_word = i * words_per_image
            end_word = start_word + words_per_image
            caption = " ".join(script_words[start_word:end_word])

            if caption:
                img = create_text_overlay(img, caption)

            frame_path = os.path.join(work_dir, f"frame_{i:04d}.jpg")
            img.save(frame_path, "JPEG", quality=70)
            frame_paths.append(frame_path)

            del img
            del img_data

        print("Assembling video with ffmpeg...")
        output_path = os.path.join(work_dir, "output.mp4")

        fps = 15
        duration_per_frame = 4
        frames_per_image = fps * duration_per_frame

        frames_dir = os.path.join(work_dir, "frames")
        os.makedirs(frames_dir, exist_ok=True)

        for i, frame_path in enumerate(frame_paths):
            abs_frame_path = os.path.abspath(frame_path)
            for j in range(frames_per_image):
                new_path = os.path.join(frames_dir, f"frame_{i * frames_per_image + j:06d}.jpg")
                os.symlink(abs_frame_path, new_path)

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", os.path.join(frames_dir, "frame_%06d.jpg"),
            "-i", audio_path,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            "-pix_fmt", "yuv420p",
            "-preset", "ultrafast",
            "-crf", "28",
            output_path
        ]

        result = subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            ffmpeg_cmd_no_audio = [
                "ffmpeg", "-y",
                "-framerate", str(fps),
                "-i", os.path.join(frames_dir, "frame_%06d.jpg"),
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "ultrafast",
                "-crf", "28",
                "-t", str(len(frame_paths) * duration_per_frame),
                output_path
            ]
            result2 = subprocess.run(
                ffmpeg_cmd_no_audio,
                capture_output=True,
                text=True,
                timeout=120
            )
            if result2.returncode != 0:
                return None, "Video assembly failed"

        print("Video generated successfully!")
        return output_path, None

    except Exception as e:
        print(f"Video generation error: {e}")
        return None, str(e)