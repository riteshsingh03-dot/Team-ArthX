import time
import json
import os
from engines.market.competitor_service import list_all_locations, refresh_competitors
from engines.market.mandi_price_service import refresh_mandi_prices
from engines.market.osm_client import fetch_distribution_channels

ALL_CATEGORIES = ["dairy", "retail", "textiles", "food_processing", "handicrafts"]
DELAY_COMPETITOR = 5   # seconds between competitor calls
DELAY_MANDI = 1
DELAY_REACH = 5
CHECKPOINT_FILE = "seed_progress.json"

def load_progress():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {"competitors_done": [], "reach_done": [], "mandi_done": []}

def save_progress(progress):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(progress, f)

progress = load_progress()
locations = list_all_locations()
print(f"{len(locations)} locations loaded.\n")

# --- PASS 1: Market Reach (once per location, not per category) ---
print("=== Market Reach pass (78 calls total) ===")
for loc in locations:
    key = str(loc["id"])
    if key in progress["reach_done"]:
        continue
    try:
        from engines.market.competitor_service import get_location
        location = get_location(loc["id"])
        channels = fetch_distribution_channels(float(location["latitude"]), float(location["longitude"]))
        print(f"  Location {loc['id']} ({loc.get('village_name')}): {channels}")
        progress["reach_done"].append(key)
        save_progress(progress)
    except Exception as e:
        print(f"  Location {loc['id']} failed: {e}")
        print("  Stopping this pass -- likely rate limited. Rerun script later to resume.")
        break
    time.sleep(DELAY_REACH)

# --- PASS 2: Competitors (per location x category -- the big one) ---
print("\n=== Competitor pass (up to 390 calls, run in chunks) ===")
for loc in locations:
    for category in ALL_CATEGORIES:
        key = f"{loc['id']}:{category}"
        if key in progress["competitors_done"]:
            continue
        try:
            result = refresh_competitors(loc["id"], category)
            print(f"  {loc.get('village_name')} / {category}: {result['competitor_count']} found")
            progress["competitors_done"].append(key)
            save_progress(progress)
        except Exception as e:
            print(f"  {loc.get('village_name')} / {category} failed: {e}")
            print("  Stopping -- rate limited. Rerun script later to resume from here.")
            exit()
        time.sleep(DELAY_COMPETITOR)

# --- PASS 3: Mandi prices (separate API, separate issue -- see note below) ---
print("\n=== Mandi price pass ===")
for loc in locations:
    for category in ALL_CATEGORIES:
        key = f"{loc['id']}:{category}"
        if key in progress["mandi_done"]:
            continue
        try:
            result = refresh_mandi_prices(loc["id"], category)
            print(f"  {loc.get('village_name')} / {category}: "
                  f"{len(result)} commodities" if result else f"  {loc.get('village_name')} / {category}: no data")
            progress["mandi_done"].append(key)
            save_progress(progress)
        except Exception as e:
            print(f"  {loc.get('village_name')} / {category} failed: {e}")
        time.sleep(DELAY_MANDI)

print("\nDone (or paused at rate limit -- rerun to resume).")