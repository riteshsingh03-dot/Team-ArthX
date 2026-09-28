import time
import requests
from sqlalchemy import text
from db.connection import engine

AREAS = [
    "Koramangala", "Indiranagar", "Whitefield", "Jayanagar",
    "HSR Layout", "Malleshwaram", "Electronic City", "Yelahanka",
]
CITY_SUFFIX = "Bengaluru, Karnataka, India"
DISTRICT = "Bangalore"   # matches Census 2011 spelling
STATE = "Karnataka"
DISTRICT_AREAS_KM2 = {"bangalore": 2190, "bangalore rural": 2259}
HEADERS = {"User-Agent": "SIH26091-BusinessAdvisor/1.0 (student project)"}


def geocode(area):
    r = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": f"{area}, {CITY_SUFFIX}", "format": "json", "limit": 1},
        headers=HEADERS, timeout=20,
    )
    r.raise_for_status()
    data = r.json()
    if not data or "karnataka" not in data[0]["display_name"].lower():
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])


def seed():
    with engine.connect() as conn:
        for area in AREAS:
            exists = conn.execute(text("""
                SELECT 1 FROM locations
                WHERE LOWER(village_name) = LOWER(:n) AND LOWER(district) = LOWER(:d)
            """), {"n": area, "d": DISTRICT}).first()
            if exists:
                print(f"  skip {area} (already in DB)")
                continue

            coords = geocode(area)
            time.sleep(1)  # Nominatim: max 1 req/sec
            if coords is None:
                print(f"  could not geocode {area}, skipping")
                continue

            conn.execute(text("""
                INSERT INTO locations (village_name, block, district, state, latitude, longitude)
                VALUES (:n, NULL, :d, :s, :lat, :lon)
            """), {"n": area, "d": DISTRICT, "s": STATE, "lat": coords[0], "lon": coords[1]})
            print(f"  inserted {area} {coords}")

        for district_name, area_km2 in DISTRICT_AREAS_KM2.items():
            conn.execute(text("""
                UPDATE census_district_population SET area_km2 = :a
                WHERE LOWER(district_name) = :n AND LOWER(state_name) = 'karnataka'
            """), {"a": area_km2, "n": district_name})
        conn.commit()
    print("Done.")


if __name__ == "__main__":
    seed()