import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://wh40k.lexicanum.com"
INDEX_URL = "https://wh40k.lexicanum.com/wiki/Loyal_Space_Marine_Chapters_(List)"

resp = requests.get(INDEX_URL, headers={"User-Agent": "LexicanumScraper/1.0"})
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# Find the sortable table
table = soup.find("table", class_="sortable")
if not table:
    raise ValueError("Could not find the sortable table on the page")

rows = table.find_all("tr")
print(f"📊 Total rows in table: {len(rows)}")

results = []

for row in rows:
    # Only take the first <td> of each row
    first_td = row.find("td")
    if first_td:
        link = first_td.find("a", href=True)
        if link and link["href"].startswith("/wiki/"):
            name = link.get_text(strip=True)
            full_url = BASE_URL + link["href"]
            results.append({"Name": name, "URL": full_url})

# Save to CSV (keeping duplicates)
with open("loyal_space_marine_chapters_first_column.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Name", "URL"])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Extracted {len(results)} entries from first column and saved to loyal_space_marine_chapters_first_column.csv")
