import requests
from bs4 import BeautifulSoup
import time
import csv
import os

# --- CONFIG ---
HEADERS = {"User-Agent": "LexicanumColourChecker/4.0 (educational use)"}
DELAY = 2  # seconds between requests
BASE_URL = "https://wh40k.lexicanum.com"

INPUT_FILE = "urls.csv"      # CSV must have a column named "URL"
OUTPUT_FILE = "results.csv"  # output file

def get_page_title(soup):
    """Extract page title like 'Andromedan Blades'."""
    title_tag = soup.find("h1", id="firstHeading")
    if title_tag:
        return title_tag.get_text(strip=True)
    # fallback: from <title> tag
    return soup.title.get_text(strip=True).replace(" - Warhammer 40k - Lexicanum", "")

def get_first_three_images(url):
    """Return the page title and up to 3 image URLs from the main infobox table."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
        return None, []

    soup = BeautifulSoup(resp.text, "html.parser")
    title = get_page_title(soup)

    tables = soup.find_all("table")
    for table in tables:
        imgs = table.find_all("img")
        if len(imgs) >= 3:
            img_urls = []
            for img in imgs[:3]:
                src = img.get("src", "")
                if not src:
                    continue
                if src.startswith("/"):
                    src = BASE_URL + src
                img_urls.append(src)
            return title, img_urls

    return title, []

def read_urls_from_csv(file_path):
    """Read a list of URLs from a CSV with a column 'URL'."""
    urls = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row.get("URL", "").strip()
            if url:
                urls.append(url)
    return urls

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Input file '{INPUT_FILE}' not found. Please create a CSV with a 'URL' column.")
        return

    urls = read_urls_from_csv(INPUT_FILE)
    print(f"📋 Loaded {len(urls)} URLs from {INPUT_FILE}\n")

    results = []

    for url in urls:
        print(f"🔍 Checking {url}")
        title, images = get_first_three_images(url)

        if not images:
            print(f"⚠️ {title}: No infobox or images found.")
            results.append({
                "Title": title,
                "URL": url,
                "Has Scheme?": "No",
                "Image 1": "",
                "Image 2": "",
                "Image 3": ""
            })
        else:
            unknown_count = sum("Unknown.jpg" in img for img in images)
            if unknown_count == 3:
                print(f"❌ {title}: All Unknown.jpg → No known scheme.")
                results.append({
                    "Title": title,
                    "URL": url,
                    "Has Scheme?": "No",
                    "Image 1": "",
                    "Image 2": "",
                    "Image 3": ""
                })
            else:
                known_imgs = [img for img in images if "Unknown.jpg" not in img]
                print(f"✅ {title}: Found {len(known_imgs)} image(s).")
                row = {
                    "Title": title,
                    "URL": url,
                    "Has Scheme?": "Yes"
                }
                for i, img in enumerate(known_imgs, start=1):
                    row[f"Image {i}"] = img
                results.append(row)

        time.sleep(DELAY)

    # --- WRITE OUTPUT ---
    fieldnames = ["Title", "URL", "Has Scheme?", "Image 1", "Image 2", "Image 3"]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Done! Results written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
