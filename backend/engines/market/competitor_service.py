from sqlalchemy import text
from db.connection import engine
from engines.market.osm_client import build_osm_dataframe


def get_location(location_id: int) -> dict:
    query = text("SELECT * FROM locations WHERE id = :id")
    with engine.connect() as conn:
        row = conn.execute(query, {"id": location_id}).mappings().first()
    if row is None:
        raise ValueError(f"No location found with id={location_id}")
    if row["latitude"] is None or row["longitude"] is None:
        raise ValueError(f"Location id={location_id} has no lat/lon on file")
    return dict(row)

def list_all_locations() -> list[dict]:
    query = text("""
        SELECT id, village_name, block, district, state
        FROM locations
        ORDER BY state, district, village_name
    """)
    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()
    return [dict(r) for r in rows]

def refresh_competitors(location_id: int, business_category: str, radius_m: int = 5000) -> dict:
    """
    Fetches live OSM competitor data for a location + category,
    stores individual rows in market_competitors, and upserts the
    aggregate count into market_seed_data.
    """
    location = get_location(location_id)
    df = build_osm_dataframe(
        lat=float(location["latitude"]),
        lon=float(location["longitude"]),
        category=business_category,
        radius_m=radius_m,
    )

    with engine.connect() as conn:
        # clear old rows for this location+category so refresh doesn't duplicate
        conn.execute(text("""
            DELETE FROM market_competitors
            WHERE location_id = :location_id AND business_category = :category
        """), {"location_id": location_id, "category": business_category})

        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO market_competitors
                (location_id, business_category, osm_place_id, name, latitude, longitude,
                 distance_km, business_status, address, phone, website, source, last_updated)
                VALUES
                (:location_id, :category, :place_id, :name, :lat, :lon,
                 :distance_km, :status, :address, :phone, :website, :source, now())
            """), {
                "location_id": location_id,
                "category": business_category,
                "place_id": row["place_id"],
                "name": row["name"],
                "lat": row["latitude"],
                "lon": row["longitude"],
                "distance_km": row["distance_km"],
                "status": row["business_status"],
                "address": row["address"],
                "phone": row["phone"],
                "website": row["website"],
                "source": row["source"],
            })

        # upsert aggregate count into market_seed_data
        existing = conn.execute(text("""
            SELECT id FROM market_seed_data
            WHERE location_id = :location_id AND business_category = :category
        """), {"location_id": location_id, "category": business_category}).first()

        if existing:
            conn.execute(text("""
                UPDATE market_seed_data
                SET competitor_count = :count, source = 'openstreetmap_overpass',
                    is_illustrative = FALSE, last_updated = CURRENT_DATE
                WHERE id = :id
            """), {"count": len(df), "id": existing[0]})
        else:
            conn.execute(text("""
                INSERT INTO market_seed_data
                (location_id, business_category, competitor_count, source, is_illustrative, last_updated)
                VALUES (:location_id, :category, :count, 'openstreetmap_overpass', FALSE, CURRENT_DATE)
            """), {"location_id": location_id, "category": business_category, "count": len(df)})

        conn.commit()

    return {
        "location_id": location_id,
        "business_category": business_category,
        "competitor_count": len(df),
        "radius_m": radius_m,
    }


def get_stored_competitors(location_id: int, business_category: str) -> list[dict]:
    query = text("""
        SELECT * FROM market_competitors
        WHERE location_id = :location_id AND business_category = :category
        ORDER BY distance_km ASC
    """)
    with engine.connect() as conn:
        rows = conn.execute(query, {"location_id": location_id, "category": business_category}).mappings().all()
    return [dict(r) for r in rows]

def resolve_location_id(village_name: str = None, block: str = None, district: str = None) -> int | None:
    """
    Best-effort match of free-text location fields against the locations table.
    Tries most specific (village) first, falls back to block, then district.
    Returns None if nothing matches -- caller must handle gracefully.
    """
    with engine.connect() as conn:
        if village_name:
            row = conn.execute(text("""
                SELECT id FROM locations
                WHERE LOWER(village_name) = LOWER(:village_name)
                LIMIT 1
            """), {"village_name": village_name}).first()
            if row:
                return row[0]

            # fuzzy fallback: partial match
            row = conn.execute(text("""
                SELECT id FROM locations
                WHERE LOWER(village_name) LIKE LOWER(:pattern)
                LIMIT 1
            """), {"pattern": f"%{village_name}%"}).first()
            if row:
                return row[0]

        if block:
            row = conn.execute(text("""
                SELECT id FROM locations
                WHERE LOWER(block) = LOWER(:block)
                LIMIT 1
            """), {"block": block}).first()
            if row:
                return row[0]

        if district:
            row = conn.execute(text("""
                SELECT id FROM locations
                WHERE LOWER(district) = LOWER(:district)
                LIMIT 1
            """), {"district": district}).first()
            if row:
                return row[0]

        # Fallback: a single ambiguous place name from extraction.py may have
        # landed in village_name even though it's actually a district-level name
        # (e.g. "Balrampur" as a district, not a specific village).
        if village_name:
            row = conn.execute(text("""
                SELECT id FROM locations
                WHERE LOWER(district) = LOWER(:village_name)
                LIMIT 1
            """), {"village_name": village_name}).first()
            if row:
                return row[0]

    return None