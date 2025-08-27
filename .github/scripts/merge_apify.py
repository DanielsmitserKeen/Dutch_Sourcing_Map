import json

# Load Apify results
with open("apify_results.json", "r", encoding="utf-8") as f:
    apify_data = json.load(f)

# Load your GeoJSON
with open("nl_earlystage_map.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Example: match Apify orgs to GeoJSON features
for feature in geojson["features"]:
    name = feature["properties"]["name"].lower()

    # Find LinkedIn posts mentioning this org
    posts = [p for p in apify_data if name in p.get("text", "").lower()]

    if posts:
        feature["properties"]["recent_posts"] = posts[:5]

# Save updated file
with open("nl_earlystage_map.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=2, ensure_ascii=False)

print("✅ GeoJSON updated with Apify results")
