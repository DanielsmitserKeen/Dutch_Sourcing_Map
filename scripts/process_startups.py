import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Load Apify results
with open("apify_results.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

# Build prompt
prompt = f"""
You are an assistant extracting startup names.
From the following LinkedIn posts, extract startup names mentioned 
in the last 4 weeks. Return ONLY JSON list with fields:
- name (startup name)
- date (post date if available)
- context (short summary why it's mentioned)
- url (link to the post if present)

Posts:
{json.dumps(posts[:20], indent=2)}
"""

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

try:
    extracted = json.loads(resp.choices[0].message.content)
except:
    extracted = []

# Load GeoJSON
with open("nl_earlystage_map.geojson", "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Attach to YES!Delft only for now
for feature in geojson["features"]:
    if feature["properties"]["name"] == "YES!Delft":
        feature["properties"]["recent_startups"] = extracted

# Save back
with open("nl_earlystage_map.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=2, ensure_ascii=False)

print("✅ GeoJSON updated with startup list for YES!Delft")
