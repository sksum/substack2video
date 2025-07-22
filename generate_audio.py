import os
import sys
import json
from pathlib import Path
from mlx_audio.tts.generate import generate_audio

# Inputs
json_path, output_dir = sys.argv[1], sys.argv[2]
Path(output_dir).mkdir(parents=True, exist_ok=True)

# Load structured blocks
with open(json_path, "r", encoding="utf-8") as f:
    blocks = json.load(f)

text_idx = 0
for block in blocks:
    if block["type"] == "text":
        output_prefix = f"{output_dir}/chunk_{text_idx:03}"
        generate_audio(
            text=block["content"],
            model_path="prince-canuma/Kokoro-82M",
            voice="af_heart",
            speed=1.2,
            lang_code="a",
            file_prefix=output_prefix,
            audio_format="wav",
            sample_rate=24000,
            join_audio=True,
            verbose=True
        )
        block["audio"] = f"{output_prefix}.wav"
        print("✅ Audio chunk saved:", block["audio"])
        text_idx += 1

# Save updated JSON with audio paths
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(blocks, f, indent=2)

print(f"\n✅ Finished generating {text_idx} audio chunks.")
