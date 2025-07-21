#!/bin/bash

# INPUT_HTML="$1"
INPUT_HTML="https://mindfulmodeler.substack.com/p/whos-really-making-the-decisions"
WORK_DIR="./output"
CHUNKS_FILE="$WORK_DIR/chunks.txt"
IMAGES_DIR="$WORK_DIR/images"
AUDIO_DIR="$WORK_DIR/audio"
mkdir -p "$WORK_DIR" "$IMAGES_DIR" "$AUDIO_DIR"

echo "[INFO] Extracting content from HTML..."
python3 extract_content.py "$INPUT_HTML" "$CHUNKS_FILE" "$IMAGES_DIR"

# echo "[INFO] Generating audio chunks..."
# python3 generate_audio.py "$CHUNKS_FILE" "$AUDIO_DIR"

# echo "[INFO] Creating video using ffmpeg..."
# python3 generate_video.py "$AUDIO_DIR" "$CHUNKS_FILE" "$IMAGES_DIR" "$WORK_DIR/final_video.mp4"

# echo "[DONE] Final video created at $WORK_DIR/final_video.mp4"
