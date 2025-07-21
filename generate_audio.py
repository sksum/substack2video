import os
import sys
from pathlib import Path
import torch
from mlx_audio import TextToSpeechPipeline

chunks_file, output_dir = sys.argv[1], sys.argv[2]
Path(output_dir).mkdir(parents=True, exist_ok=True)

pipeline = TextToSpeechPipeline(model_id="kokkoro-tts/kokkoro")

with open(chunks_file) as f:
    lines = [line.strip() for line in f if line.strip()]

for idx, text in enumerate(lines):
    wav = pipeline.synthesize(text)
    output_path = f"{output_dir}/chunk_{idx:03}.wav"
    pipeline.save_audio(wav, output_path)
