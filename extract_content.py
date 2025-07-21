import sys, os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from pathlib import Path

html_path, output_txt, img_dir = sys.argv[1], sys.argv[2], sys.argv[3]
response = requests.get(html_path)
html = response.text
base_url = html_path 
soup = BeautifulSoup(html, "html.parser")
content = soup.find(class_="available-content")

text_blocks = []
img_urls = []

for elem in content.find_all(["p", "img"]):
    if elem.name == "p" and elem.text.strip():
        text_blocks.append(elem.text.strip())
    elif elem.name == "img" and elem.get("src"):
        img_urls.append(elem["src"])

# Save text chunks
with open(output_txt, "w") as f:
    for block in text_blocks:
        f.write(block + "\n")

# Download images
Path(img_dir).mkdir(parents=True, exist_ok=True)
for i, url in enumerate(img_urls):
    img_data = requests.get(urljoin(html_path, url)).content
    with open(f"{img_dir}/img_{i:03}.jpg", "wb") as handler:
        handler.write(img_data)
