import sys, os, json
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from pathlib import Path

# Inputs: html_url, output_json_file, image_output_dir
html_url, output_json, img_dir = sys.argv[1], sys.argv[2], sys.argv[3]
response = requests.get(html_url)
html = response.text

soup = BeautifulSoup(html, "html.parser")
content = soup.find(class_="available-content")

if not content:
    print("❌ Could not find .available-content in the HTML.")
    sys.exit(1)

Path(img_dir).mkdir(parents=True, exist_ok=True)

blocks = []
img_counter = 0

for elem in content.find_all(["p", "img"]):
    if elem.name == "p":
        text = elem.get_text(strip=True)
        if text:
            blocks.append({"type": "text", "content": text})
    elif elem.name == "img" and elem.get("src"):
        img_url = urljoin(html_url, elem["src"])
        img_filename = f"{img_dir}/img_{img_counter:03}.jpg"

        try:
            img_data = requests.get(img_url).content
            with open(img_filename, "wb") as f:
                f.write(img_data)
            blocks.append({"type": "image", "path": img_filename})
            img_counter += 1
        except Exception as e:
            print(f"⚠️ Failed to download image from {img_url}: {e}")

# Save ordered blocks to JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(blocks, f, indent=2)

print(f"✅ Extracted {len(blocks)} content blocks ({img_counter} images).")
