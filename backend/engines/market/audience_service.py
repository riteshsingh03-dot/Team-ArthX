from sqlalchemy import text
from db.connection import engine
import math

AVG_HOUSEHOLD_SIZE = 4.5  # rural India average; override per-state if you find a better figure

# Keyed lowercase/underscored to match business_knowledge.py's category keys --
# NOT the Title Case names ("Dairy", "Retail") from the original notebook.
# Tailoring/Mobile Repair/Food-Snack from the notebook don't map 1:1 onto your
# app's categories (dairy/retail/textiles/food_processing/handicrafts), so these
# are approximated -- tune them once you have real local data.

URBAN_HOUSEHOLD_SIZE = 4.0
CATCHMENT_RADIUS_KM = 2  # must match the 2000 m radius in competitor_service
PLACE_ALIASES = {
    "bengaluru": "bangalore",
    "bengaluru urban": "bangalore",
    "bengaluru rural": "bangalore rural",
}

CATEGORY_PENETRATION = {
    "dairy": 0.85,
    "retail": 0.95,
    "textiles": 0.15,
    "food_processing": 0.30,
    "handicrafts": 0.10,
}
DEFAULT_PENETRATION = 0.20


def _get_penetration(business_category: str) -> float:
    key = (business_category or "").strip().lower().replace(" ", "_")
    return CATEGORY_PENETRATION.get(key, DEFAULT_PENETRATION)


def get_district_population(district: str) -> dict | None:
    """Best-effort match against the seeded census_district_population table."""
    if not district:
        return None
    
    district = PLACE_ALIASES.get(district.strip().lower(), district)
    with engine.connect() as conn:
        row = conn.execute(text("""
            SELECT * FROM census_district_population
            WHERE LOWER(district_name) = LOWER(:district)
            LIMIT 1
        """), {"district": district}).mappings().first()
        if row is None:
            row = conn.execute(text("""
                SELECT * FROM census_district_population
                WHERE LOWER(district_name) LIKE LOWER(:pattern)
                LIMIT 1
            """), {"pattern": f"%{district}%"}).mappings().first()
    return dict(row) if row else None


def estimate_target_audience(population: int, business_category: str, competitor_count: int,
                             area_km2: float | None = None) -> dict:
    penetration = _get_penetration(business_category)

    if area_km2:
        density = population / float(area_km2)
        catchment_km2 = math.pi * CATCHMENT_RADIUS_KM ** 2
        local_population = density * catchment_km2
        household_size = URBAN_HOUSEHOLD_SIZE
        scope = f"catchment_{CATCHMENT_RADIUS_KM}km"
    else:
        local_population = population
        household_size = AVG_HOUSEHOLD_SIZE
        scope = "district"

    households = local_population / household_size
    addressable_households = households * penetration
    estimated_customers = addressable_households / (competitor_count + 1)

    result = {
        "total_population": int(local_population),
        "estimated_households": int(households),
        "addressable_households": int(addressable_households),
        "existing_competitors": competitor_count,
        "estimated_customers_for_you": int(estimated_customers),
        "population_scope": scope,
    }
    if area_km2:
        result["population_density_per_km2"] = int(density)
        result["catchment_area_km2"] = round(catchment_km2, 1)
    return result


def get_target_audience_mapping(district: str | None, business_category: str | None,
                                 competitor_count: int | None) -> dict | None:
    """
    Main entry point for main.py/swot.py. Never raises -- missing district,
    no census match, or bad inputs all degrade to None.
    Pass in the competitor_count you already computed via get_competitor_mapping()
    rather than triggering a second OSM fetch here.
    """
    if not district or business_category is None:
        return None
    try:
        census = get_district_population(district)
        if census is None or census.get("population") is None:
            return None
        return estimate_target_audience(
            population=census["population"],
            business_category=business_category,
            competitor_count=competitor_count or 0,
            area_km2=census.get("area_km2"),
        )
    except (ValueError, TypeError):
        return None