from engines.llm.business_knowledge import BUSINESS_CATEGORY_NOTES, get_category_notes
from engines.llm.swot import generate_swot
from engines.financial.loan import calculate_loan_structure
from engines.market.mandi_price_service import get_mandi_price_mapping
from engines.market.audience_service import get_target_audience_mapping
from engines.market.competitor_service import get_stored_competitors, refresh_competitors, get_location
from google.genai.errors import ServerError

ALL_CATEGORIES = list(BUSINESS_CATEGORY_NOTES.keys())


def _get_competitor_mapping(location_id, category):
    if location_id is None:
        return None
    try:
        rows = get_stored_competitors(location_id, category)
        if not rows:
            refresh_competitors(location_id, category)
            rows = get_stored_competitors(location_id, category)
        return {"competitor_count": len(rows), "nearest": rows[:5]}
    except (ValueError, RuntimeError):
        return None


def _get_audience_mapping(location_id, district, village_name, category, competitor_mapping):
    fallback = district or village_name
    if location_id is not None:
        try:
            location = get_location(location_id)
            fallback = location.get("district") or fallback
        except ValueError:
            pass
    competitor_count = competitor_mapping.get("competitor_count") if competitor_mapping else None
    return get_target_audience_mapping(fallback, category, competitor_count)


def _score_category(competitor_mapping, audience_mapping):
    """
    Simple, transparent fit score: more estimated customers per competitor = better.
    Returns a float score, higher is better. Missing data -> lowest priority, not an error.
    """
    if not audience_mapping:
        return -1
    if competitor_mapping is None:
        return -1  # unknown competitor data -> don't let it win by default
    estimated_customers = audience_mapping.get("estimated_customers_for_you", 0)
    competitor_count = competitor_mapping.get("competitor_count") or 0
    return estimated_customers - (competitor_count * 5)


def rank_sectors(
    location_id: int | None,
    project_cost: float,
    margin_pct: float,
    district: str | None = None,
    village_name: str | None = None,
    categories: list[str] | None = None,
    experience_level: str = "intermediate",
    top_n_for_swot: int = 3,
) -> list[dict]:
    """
    Runs lightweight market-fit scoring across all candidate categories using
    data already fetched elsewhere (OSM competitors, census audience, mandi
    price). Returns all categories ranked; only the top `top_n_for_swot`
    get a full SWOT generated (LLM calls are the expensive part).
    """
    categories = categories or ALL_CATEGORIES
    loan = calculate_loan_structure(project_cost, margin_pct)

    results = []
    for category in categories:
        competitor_mapping = _get_competitor_mapping(location_id, category)
        audience_mapping = _get_audience_mapping(location_id, district, village_name, category, competitor_mapping)
        mandi_mapping = get_mandi_price_mapping(location_id, category)
        category_notes = get_category_notes(category)

        results.append({
            "business_category": category,
            "competitor_mapping": competitor_mapping,
            "audience_mapping": audience_mapping,
            "mandi_mapping": mandi_mapping,
            "category_notes": category_notes,
            "fit_score": _score_category(competitor_mapping, audience_mapping),
        })

    results.sort(key=lambda r: r["fit_score"], reverse=True)

    for r in results[:top_n_for_swot]:
        try:
            r["swot"] = generate_swot(
                business_category=r["business_category"],
                project_cost=project_cost,
                loan_amount=loan["loan_amount"],
                location={
                    "village_name": village_name,
                    "block": None,
                    "district": district,
                    "state": None,
                },
                experience_level=experience_level,
                competitor_mapping=r["competitor_mapping"],
                mandi_mapping=r["mandi_mapping"],
                audience_mapping=r["audience_mapping"],
            )
        except ServerError:
            r["swot"] = None
            r["swot_error"] = "AI analysis temporarily unavailable for this category. Try again in a moment."

    return results