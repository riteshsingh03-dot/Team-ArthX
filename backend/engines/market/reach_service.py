import math
from engines.market.osm_client import fetch_distribution_channels
from engines.market.audience_service import _get_penetration, AVG_HOUSEHOLD_SIZE, get_district_population

DEFAULT_RADIUS_M = 7500  # midpoint of PS-specified 5-10km range
TYPICAL_DISTRICT_AREA_KM2 = 1500  # rough rural Indian district area; illustrative scaling only


def estimate_local_reach(lat, lon, district, business_category, competitor_count, radius_m=DEFAULT_RADIUS_M):
    """
    Hyperlocal (radius-based) reach estimate: distribution channels are real
    OSM data; population is a scaled-down illustrative approximation from
    district-level census data, not a true radius-level count -- flagged
    accordingly, consistent with mandi/competitor illustrative-data pattern.
    """
    channels = fetch_distribution_channels(lat, lon, radius_m)

    census = get_district_population(district) if district else None
    if census is None or census.get("population") is None:
        return {
            "radius_km": radius_m / 1000,
            "distribution_channels": channels,
            "estimated_local_population": None,
            "is_illustrative": True,
            "note": "No district population data available for this location.",
        }

    radius_km = radius_m / 1000
    circle_area_km2 = math.pi * (radius_km ** 2)
    area_ratio = min(circle_area_km2 / TYPICAL_DISTRICT_AREA_KM2, 1.0)
    local_population = census["population"] * area_ratio

    households = local_population / AVG_HOUSEHOLD_SIZE
    penetration = _get_penetration(business_category)
    addressable_households = households * penetration
    total_players = (competitor_count or 0) + 1
    estimated_customers = addressable_households / total_players

    return {
        "radius_km": radius_km,
        "distribution_channels": channels,
        "estimated_local_population": int(local_population),
        "estimated_customers_for_you": int(estimated_customers),
        "is_illustrative": True,
        "note": "Population scaled from district-level census by area ratio, not a direct radius-level count.",
    }


def get_market_reach_mapping(location_id, district, business_category, competitor_count):
    """
    Main entry point for main.py. Never raises -- missing location, bad
    coordinates, or Overpass failure all degrade to None.
    """
    if location_id is None:
        return None
    try:
        from engines.market.competitor_service import get_location
        location = get_location(location_id)
        return estimate_local_reach(
            lat=float(location["latitude"]),
            lon=float(location["longitude"]),
            district=district,
            business_category=business_category,
            competitor_count=competitor_count,
        )
    except (ValueError, RuntimeError, TypeError):
        return None