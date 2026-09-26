import os
import time
import requests
from dotenv import load_dotenv
from sqlalchemy import text
from db.connection import engine
from engines.market.competitor_service import get_location
from engines.llm.business_knowledge import get_mandi_commodities

load_dotenv()

MANDI_API_KEY = os.environ.get("MANDI_API_KEY")
MANDI_RESOURCE_ID = os.environ.get("MANDI_RESOURCE_ID", "9ef84268-d588-465a-a308-a864a43d0070")
MANDI_BASE_URL = f"https://api.data.gov.in/resource/{MANDI_RESOURCE_ID}"

DEFAULT_CACHE_DAYS = 7  # mandi prices move faster than competitor counts -- shorter cache


def _require_api_key():
    if not MANDI_API_KEY:
        raise RuntimeError(
            "MANDI_API_KEY is not set. Add it to your .env file -- "
            "get a free key at https://data.gov.in/user/register "
            "(the public sample key is heavily rate-limited and will hang/timeout)."
        )


def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fetch_mandi_records(state: str, district: str, commodity: str,
                         limit: int = 200, max_records: int = 1000,
                         retries: int = 3, timeout: int = 15) -> list[dict]:
    """
    Pulls records for one commodity from the data.gov.in mandi-prices resource.
    Bounded retries + a real timeout so a slow API degrades instead of hanging
    the request thread (this is what hung indefinitely in the notebook).
    """
    _require_api_key()
    all_records = []
    offset = 0

    while offset < max_records:
        params = {
            "api-key": MANDI_API_KEY,
            "format": "json",
            "limit": limit,
            "offset": offset,
            "filters[state]": state,
            "filters[district]": district,
            "filters[commodity]": commodity,
        }

        data = None
        for attempt in range(retries):
            try:
                r = requests.get(MANDI_BASE_URL, params=params, timeout=timeout)
                if r.status_code == 200:
                    data = r.json()
                    break
            except requests.exceptions.RequestException:
                pass
            time.sleep(2 * (attempt + 1))

        if data is None:
            break  # give up on this commodity rather than blocking the request

        records = data.get("records", [])
        if not records:
            break
        all_records.extend(records)
        offset += limit
        if len(records) < limit:
            break

    return all_records


def _get_cached_avg(location_id: int, business_category: str, max_age_days: int) -> list[dict]:
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT commodity, avg_modal_price, sample_size FROM mandi_prices_avg
            WHERE location_id = :location_id AND business_category = :category
              AND last_updated >= CURRENT_DATE - :max_age_days
        """), {"location_id": location_id, "category": business_category, "max_age_days": max_age_days}).mappings().all()
    return [dict(r) for r in rows]


def refresh_mandi_prices(location_id: int, business_category: str) -> list[dict]:
    """
    Fetches live mandi prices for every commodity mapped to this business
    category, stores raw + averaged rows, returns the averaged rows.
    Returns [] (not an exception) if the category has no mandi-relevant
    commodities, the location lacks state/district, or every fetch fails.
    """
    commodities = get_mandi_commodities(business_category)
    if not commodities:
        return []

    location = get_location(location_id)
    state = location.get("state")
    district = location.get("district")
    if not state or not district:
        return []

    averages = []
    with engine.connect() as conn:
        for commodity in commodities:
            records = fetch_mandi_records(state=state, district=district, commodity=commodity)
            if not records:
                continue

            modal_prices = [p for p in (_to_float(r.get("modal_price")) for r in records) if p is not None]

            for r in records:
                conn.execute(text("""
                    INSERT INTO mandi_prices_raw
                    (location_id, business_category, commodity, market_name, state, district,
                     min_price, max_price, modal_price, arrival_date, source)
                    VALUES
                    (:location_id, :category, :commodity, :market_name, :state, :district,
                     :min_price, :max_price, :modal_price, :arrival_date, 'data_gov_in_agmarknet')
                """), {
                    "location_id": location_id,
                    "category": business_category,
                    "commodity": commodity,
                    "market_name": r.get("market"),
                    "state": r.get("state"),
                    "district": r.get("district"),
                    "min_price": _to_float(r.get("min_price")),
                    "max_price": _to_float(r.get("max_price")),
                    "modal_price": _to_float(r.get("modal_price")),
                    "arrival_date": r.get("arrival_date"),
                })

            if not modal_prices:
                continue

            avg_price = round(sum(modal_prices) / len(modal_prices), 2)

            conn.execute(text("""
                INSERT INTO mandi_prices_avg
                    (location_id, business_category, commodity, avg_modal_price, sample_size, is_illustrative, last_updated)
                VALUES
                    (:location_id, :category, :commodity, :avg_price, :sample_size, FALSE, CURRENT_DATE)
                ON CONFLICT (location_id, business_category, commodity)
                DO UPDATE SET avg_modal_price = :avg_price, sample_size = :sample_size,
                              is_illustrative = FALSE, last_updated = CURRENT_DATE
            """), {
                "location_id": location_id,
                "category": business_category,
                "commodity": commodity,
                "avg_price": avg_price,
                "sample_size": len(modal_prices),
            })

            averages.append({"commodity": commodity, "avg_modal_price": avg_price, "sample_size": len(modal_prices)})

        conn.commit()

    return averages


def get_mandi_price_mapping(location_id: int | None, business_category: str | None,
                             max_age_days: int = DEFAULT_CACHE_DAYS) -> dict | None:
    """
    Main entry point for main.py / swot.py.
    Returns {"avg_price": float, "commodities": [...]} or None.
    Never raises -- missing key, no mapping, or network failure all degrade to None
    so a mandi outage never breaks /chat or /feasibility.
    """
    if location_id is None or business_category is None:
        return None
    try:
        rows = _get_cached_avg(location_id, business_category, max_age_days)
        if not rows:
            rows = refresh_mandi_prices(location_id, business_category)
        if not rows:
            return None

        prices = [r["avg_modal_price"] for r in rows if r.get("avg_modal_price") is not None]
        if not prices:
            return None

        return {
            "avg_price": round(sum(prices) / len(prices), 2),
            "commodities": rows,
        }
    except (ValueError, RuntimeError) as e:
        print(f"[DEBUG mandi_price_service] Failed: {e}")
        return None