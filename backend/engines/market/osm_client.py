"""
osm_competitor_fetch.py

Fetches nearby businesses using OpenStreetMap's Overpass API.
No API key, no billing account, no signup required -- this hits a
public Overpass endpoint directly.

Setup:
    pip install requests pandas

Usage:
    python osm_competitor_fetch.py

How category matching works:
    OSM tags businesses with keys like shop=dairy, amenity=cafe,
    shop=supermarket, etc. Rather than free-text categories like
    Gemini/Places use, you give this script an OSM tag filter. A
    small CATEGORY_PRESETS dict below maps common everyday category
    names (like "dairy shop", "cafe", "pharmacy") to the right OSM
    tag -- extend it as needed for your use case.

Caveats (read before relying on this for real decisions):
1. Data is crowd-sourced. Coverage is excellent in many cities but
   can be sparse or stale in less-mapped areas -- ALWAYS spot-check
   important results.
2. No ratings/reviews/review counts -- OSM doesn't track that.
   Phone/website are present only when someone bothered to tag them.
3. "business_status" is inferred from the disused:/was: tag prefix
   convention, which isn't universally used -- treat as best-effort.
4. Distance is computed with the haversine formula (straight-line,
   not walking/driving distance).
"""

import time
import math
import requests
import pandas as pd
from datetime import datetime, timezone

OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",  # fallback mirror
]

COLUMNS = [
    "place_id", "name", "category", "latitude", "longitude", "distance_km",
    "rating", "review_count", "business_status", "address", "phone",
    "website", "source", "last_updated", "confidence",
]

# Map friendly category names -> OSM tag (key, value).
# Extend this as you need more categories.
CATEGORY_PRESETS = {
    "dairy shop": ("shop", "dairy"),
    "dairy": ("shop", "dairy"), 
    "cafe": ("amenity", "cafe"),
    "restaurant": ("amenity", "restaurant"),
    "bakery": ("shop", "bakery"),
    "supermarket": ("shop", "supermarket"),
    "convenience store": ("shop", "convenience"),
    "retail": ("shop", "convenience"),
    "pharmacy": ("amenity", "pharmacy"),
    "clothing store": ("shop", "clothes"),
    "textiles": ("shop", "clothes"), 
    "hardware store": ("shop", "hardware"),
    "electronics store": ("shop", "electronics"),
    "gym": ("leisure", "fitness_centre"),
    "salon": ("shop", "hairdresser"),
    "bookstore": ("shop", "books"),
    "food_processing": ("shop", "farm"),
    "handicrafts": ("shop", "gift"), 
}

DISTRIBUTION_CHANNEL_TAGS = [
    ("highway", "bus_stop"),
    ("amenity", "bus_station"),
    ("amenity", "marketplace"),
    ("highway", "primary"),
    ("highway", "secondary"),
]

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def resolve_category(category):
    """
    Looks up a friendly category name in CATEGORY_PRESETS. If not
    found, tries to use it directly as a shop=<category> tag (works
    for many OSM shop values like 'shop=bicycle', 'shop=jewelry').
    """
    key = category.strip().lower()
    if key in CATEGORY_PRESETS:
        return CATEGORY_PRESETS[key]
    # Fallback: assume it's a shop=* value the user already knows.
    guess = key.replace(" ", "_")
    print(f"[info] '{category}' not in CATEGORY_PRESETS -- guessing tag "
          f"shop={guess}. Add it to CATEGORY_PRESETS if this is wrong.")
    return ("shop", guess)


def _run_overpass_query(query, timeout=30, max_retries_per_endpoint=2):
    """
    Tries each endpoint in turn. On 429 (rate limited) specifically, retries
    the SAME endpoint with exponential backoff (2s, 4s) before giving up on
    it and moving to the next mirror -- a plain sleep(1) isn't enough to
    clear a real rate limit and just burns through both mirrors instantly.
    """
    last_err = None
    for endpoint in OVERPASS_ENDPOINTS:
        for attempt in range(max_retries_per_endpoint):
            try:
                resp = requests.post(endpoint, data={"data": query}, timeout=timeout)
                if resp.status_code == 200:
                    return resp.json()
                if resp.status_code == 429:
                    wait = 2 * (2 ** attempt)  # 2s, 4s
                    last_err = RuntimeError(f"{endpoint} returned HTTP 429 (rate limited)")
                    time.sleep(wait)
                    continue
                # non-429 error -- no point retrying this endpoint, move on
                last_err = RuntimeError(f"{endpoint} returned HTTP {resp.status_code}")
                break
            except requests.RequestException as e:
                last_err = e
                break
        time.sleep(1)  # be polite before trying the next mirror
    raise RuntimeError(f"All Overpass endpoints failed. Last error: {last_err}")


def fetch_osm_nearby(lat, lon, category, radius_m=5000):
    """
    Queries Overpass for nodes/ways/relations matching the resolved
    OSM tag within radius_m of (lat, lon). Returns the raw Overpass
    JSON response.
    """
    tag_key, tag_val = resolve_category(category)

    # nwr = node/way/relation, searches all three geometry types.
    query = f"""
    [out:json][timeout:25];
    (
      nwr["{tag_key}"="{tag_val}"](around:{radius_m},{lat},{lon});
    );
    out center tags;
    """
    return _run_overpass_query(query)


def _extract_address(tags):
    parts = []
    if tags.get("addr:housenumber"):
        parts.append(tags["addr:housenumber"])
    if tags.get("addr:street"):
        parts.append(tags["addr:street"])
    if tags.get("addr:city"):
        parts.append(tags["addr:city"])
    if tags.get("addr:postcode"):
        parts.append(tags["addr:postcode"])
    return ", ".join(parts) if parts else None


def _business_status(tags):
    # OSM convention: disused:shop=*, was:shop=*, etc. mark closed places.
    for k in tags:
        if k.startswith("disused:") or k.startswith("was:"):
            return "CLOSED_OR_DISUSED"
    return "OPERATIONAL"


def build_osm_dataframe(lat, lon, category, radius_m=5000):
    data = fetch_osm_nearby(lat, lon, category, radius_m)
    elements = data.get("elements", [])
    now_iso = datetime.now(timezone.utc).isoformat()

    rows = []
    for el in elements:
        tags = el.get("tags", {})
        name = tags.get("name")
        if not name:
            continue  # skip unnamed nodes -- not useful as a competitor row

        # Nodes have lat/lon directly; ways/relations have a "center".
        if el["type"] == "node":
            p_lat, p_lon = el.get("lat"), el.get("lon")
        else:
            center = el.get("center", {})
            p_lat, p_lon = center.get("lat"), center.get("lon")

        if p_lat is None or p_lon is None:
            continue

        dist_km = round(haversine_km(lat, lon, p_lat, p_lon), 3)

        rows.append({
            "place_id": f"osm_{el['type']}_{el['id']}",
            "name": name,
            "category": category,
            "latitude": p_lat,
            "longitude": p_lon,
            "distance_km": dist_km,
            "rating": None,          # OSM has no ratings
            "review_count": None,    # OSM has no reviews
            "business_status": _business_status(tags),
            "address": _extract_address(tags),
            "phone": tags.get("phone") or tags.get("contact:phone"),
            "website": tags.get("website") or tags.get("contact:website"),
            "source": "openstreetmap_overpass",
            "last_updated": now_iso,
            "confidence": 0.7,  # decent -- has real coords, but crowd-sourced/no ratings
        })

    df = pd.DataFrame(rows, columns=COLUMNS)
    if not df.empty:
        df = df.sort_values("distance_km").reset_index(drop=True)
    return df

def fetch_distribution_channels(lat, lon, radius_m=7500):
    """
    Queries Overpass for distribution-channel infrastructure (bus stops,
    bus stations, marketplaces, primary/secondary roads) within radius_m
    of (lat, lon). Returns counts by channel type, not individual records --
    Market Reach only needs density, not a stored dataframe.
    """
    filters = "".join(
        f'nwr["{k}"="{v}"](around:{radius_m},{lat},{lon});\n'
        for k, v in DISTRIBUTION_CHANNEL_TAGS
    )
    query = f"""
    [out:json][timeout:25];
    (
    {filters}
    );
    out center tags;
    """
    data = _run_overpass_query(query)
    elements = data.get("elements", [])

    counts = {"bus_stops": 0, "bus_stations": 0, "markets": 0, "main_roads": 0}
    for el in elements:
        tags = el.get("tags", {})
        if tags.get("highway") == "bus_stop":
            counts["bus_stops"] += 1
        elif tags.get("amenity") == "bus_station":
            counts["bus_stations"] += 1
        elif tags.get("amenity") == "marketplace":
            counts["markets"] += 1
        elif tags.get("highway") in ("primary", "secondary"):
            counts["main_roads"] += 1

    return counts