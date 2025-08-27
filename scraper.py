import requests
from bs4 import BeautifulSoup
import json

def scrape_yesdelft():
    url = "https://www.yesdelft.com/startups/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    startups = []
    for card in soup.select("div.company-item"):
        name = card.get_text(strip=True)
        link = card.find("a")["href"] if card.find("a") else None
        startups.append({"name": name, "url": link})
    return startups

# Load your GeoJSON
with open("nl_earlystage_map.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

# Update YES!Delft entry
startups = scrape_yesdelft()
for feature in data["features"]:
    if feature["properties"]["name"] == "YES!Delft":
        feature["properties"]["startups"] = json.dumps(startups[:10])  # save last 10

# Save updated file
with open("nl_earlystage_map.geojson", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ GeoJSON updated with YES!Delft startups")
