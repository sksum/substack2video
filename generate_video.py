import os
import sys
import json
import subprocess
from pathlib import Path
import wave

def get_audio_duration_wav(file_path):
    with wave.open(file_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / float(rate)

def format_srt_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

# === Inputs ===
json_path = sys.argv[1]
output_path = sys.argv[2]

# === Temp directory for intermediate files ===
temp_dir = "output/temp_video"
Path(temp_dir).mkdir(parents=True, exist_ok=True)

# === Load the structured JSON ===
with open(json_path, "r", encoding="utf-8") as f:
    blocks = json.load(f)

# === Group content under each image ===
segments = []
current_image = None
current_texts = []
current_audios = []

for block in blocks:
    if block["type"] == "image":
        if current_texts and current_image:
            segments.append((current_image, current_texts, current_audios))
            current_texts, current_audios = [], []
        current_image = block["path"]
    elif block["type"] == "text" and "audio" in block:
        current_texts.append(block["content"])
        current_audios.append(block["audio"])

# Final segment
if current_texts and current_image:
    segments.append((current_image, current_texts, current_audios))

# === Build video segments ===
video_list_path = os.path.join(temp_dir, "video_list.txt")
with open(video_list_path, "w") as vf:
    for idx, (img_path, texts, audios) in enumerate(segments):
        print(f"🎞️  Building segment {idx}...")

        # -- Concatenate audio --
        audio_list_file = os.path.join(temp_dir, f"audio_list_{idx:03}.txt")
        audio_concat_path = os.path.join(temp_dir, f"audio_concat_{idx:03}.wav")

        with open(audio_list_file, "w") as af:
            for audio in audios:
                af.write(f"file '{os.path.abspath(audio)}'\n")

        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", audio_list_file,
            "-c", "copy", audio_concat_path
        ], check=True)

        # -- Build SRT file --
        srt_path = os.path.join(temp_dir, f"segment_{idx:03}.srt")
        with open(srt_path, "w", encoding="utf-8") as srt:
            current_time = 0.0
            for i, (text, audio_file) in enumerate(zip(texts, audios)):
                duration = get_audio_duration_wav(audio_file)
                start = format_srt_timestamp(current_time)
                end = format_srt_timestamp(current_time + duration)
                srt.write(f"{i+1}\n{start} --> {end}\n{text}\n\n")
                current_time += duration

        # -- Build video with subtitles --
        segment_video = os.path.join(temp_dir, f"segment_{idx:03}.mp4")
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", os.path.abspath(img_path),
            "-i", audio_concat_path,
            "-vf", f"subtitles='{srt_path}'",
            "-shortest", "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k", segment_video
        ], check=True)

        vf.write(f"file '{os.path.abspath(segment_video)}'\n")

# === Final concat ===
print("🎬 Concatenating all segments into final video...")
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", video_list_path, "-c", "copy", output_path
], check=True)

print(f"\n✅ Final video saved to: {output_path}")
