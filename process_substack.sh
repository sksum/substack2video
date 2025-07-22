#!/bin/bash

# INPUT_HTML="$1"
INPUT_HTML="https://www.interconnects.ai/p/latest-open-artifacts-12-qwen3-235b-a22b-instruct-2507?utm_source=substack&publication_id=48206&post_id=168882114&utm_medium=email&utm_content=share&utm_campaign=email-share&triggerShare=true&isFreemail=true&r=17hhfn&triedRedirect=true"
WORK_DIR="./output"
CHUNKS_FILE="$WORK_DIR/chunks.txt"
IMAGES_DIR="$WORK_DIR/images"
AUDIO_DIR="$WORK_DIR/audio"
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR" "$IMAGES_DIR" "$AUDIO_DIR"

echo "[INFO] Extracting content from HTML..."
python extract_content.py "$INPUT_HTML" "$CHUNKS_FILE" "$IMAGES_DIR"

echo "[INFO] Generating audio chunks..."
python generate_audio.py "$CHUNKS_FILE" "$AUDIO_DIR"

echo "[INFO] Creating video using ffmpeg..."
python generate_video.py "$CHUNKS_FILE" "$WORK_DIR/final_video.mp4"

echo "[DONE] Final video created at $WORK_DIR/final_video.mp4"
mpv "$WORK_DIR/final_video.mp4" 
