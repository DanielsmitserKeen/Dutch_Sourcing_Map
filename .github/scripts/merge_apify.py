import json

# Load existing GeoJSON
with open("nl_earlystage_map.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Load Apify results
with open("apify_results.json", "r", encoding="utf-8") as f:
    apify_data = json.load(f)

# Group posts by company/page
posts_by_company = {}
for item in apify_data:
    company = item.get("profileName") or item.get("authorName") or "Unknown"
    post = {
        "name": item.get("text", "Untitled Post")[:80] + "...",
        "url": item.get("url", "#"),
        "date": item.get("time", "")
    }
    posts_by_company.setdefault(company, []).append(post)

# Inject posts into GeoJSON features
for feature in geojson["features"]:
    name = feature["properties"]["name"]
    # Try to match YES!Delft etc. with scraped posts
    if "YES!Delft" in name and "YES!Delft" in posts_by_company:
        feature["properties"]["recent_posts"] = posts_by_company["YES!Delft"]
    elif "UtrechtInc" in name and "UtrechtInc" in posts_by_company:
        feature["properties"]["recent_posts"] = posts_by_company["UtrechtInc"]
    elif "Rockstart" in name and "Rockstart" in posts_by_company:
        feature["properties"]["recent_posts"] = posts_by_company["Rockstart"]

# Save updated GeoJSON
with open("nl_earlystage_map.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=2)
