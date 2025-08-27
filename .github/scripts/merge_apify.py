import json

# Load Apify results
with open("apify_results.json", "r", encoding="utf-8") as f:
    apify_data = json.load(f)

# Load GeoJSON
with open("nl_earlystage_map.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Group posts by profileName (Apify field)
posts_by_company = {}
for item in apify_data:
    company = item.get("profileName", "").strip()
    post = {
        "name": item.get("text", "Untitled Post"),
        "url": item.get("url", "#"),
        "date": item.get("time", "")
    }
    if company:
        posts_by_company.setdefault(company, []).append(post)

# Attach posts into matching features in GeoJSON
for feature in geojson["features"]:
    org_name = feature["properties"].get("name", "").strip()
    if org_name in posts_by_company:
        feature["properties"]["recent_posts"] = posts_by_company[org_name][:5]  # limit to 5

# Save updated GeoJSON
with open("nl_earlystage_map.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=2, ensure_ascii=False)

print("✅ GeoJSON updated with recent posts from Apify")
