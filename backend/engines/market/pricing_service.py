from engines.market.mandi_price_service import get_mandi_price_mapping

GENERALIZED_PRICE_RANGES = {
    "dairy": (40, 60),
    "retail": (20, 200),
    "textiles": (150, 500),
    "food_processing": (50, 150),
    "handicrafts": (100, 400),
}
DEFAULT_RANGE = (50, 150)


def _competitor_multiplier(competitor_count):
    if competitor_count is None:
        return 1.0
    if competitor_count == 0:
        return 1.15
    if competitor_count <= 4:
        return 1.05
    return 0.95


def get_price_suggestion(location_id, district, business_category, competitor_count=None):
    mandi_mapping = get_mandi_price_mapping(location_id, business_category)

    if mandi_mapping and mandi_mapping.get("avg_price"):
        multiplier = _competitor_multiplier(competitor_count)
        suggested_price = round(mandi_mapping["avg_price"] * multiplier, 2)
        return {
            "suggested_price": suggested_price,
            "avg_market_price": mandi_mapping["avg_price"],
            "competitor_adjustment_multiplier": multiplier,
            "based_on": "local_mandi_data",
            "is_illustrative": False,
            "commodities": mandi_mapping.get("commodities", []),
        }

    key = (business_category or "").strip().lower().replace(" ", "_")
    low, high = GENERALIZED_PRICE_RANGES.get(key, DEFAULT_RANGE)
    suggested_price = round((low + high) / 2, 2)

    return {
        "suggested_price": suggested_price,
        "price_range": [low, high],
        "based_on": "generalized_category_estimate",
        "is_illustrative": True,
        "note": "We don't have local market price data for your area yet. "
                "This is a generalized estimate based on typical pricing for this "
                "business category, not your specific location.",
    }