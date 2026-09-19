import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from engines.llm.business_knowledge import get_category_notes
from engines.llm.explanation import EXPERIENCE_STYLE_GUIDANCE
import time
from google.genai.errors import ServerError

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def call_gemini_with_retry(fn, *args, retries=2, base_delay=3, **kwargs):
    for attempt in range(retries + 1):
        try:
            return fn(*args, **kwargs)
        except ServerError:
            if attempt == retries:
                raise
            time.sleep(base_delay * (attempt + 1))

SWOT_PROMPT = """
You are generating a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
for a rural micro-entrepreneur, based ONLY on the facts given below. Do NOT invent
statistics, competitor numbers, or prices not present in this data. If a data point
is marked "illustrative", treat it as an example figure and note that in your output
where relevant rather than presenting it as confirmed fact.

BUSINESS CATEGORY: {business_category}
LOCATION: {village_name}, {block}, {district}, {state}
PROJECT COST: {project_cost}
LOAN AMOUNT: {loan_amount}

LOCAL MARKET DATA (illustrative unless stated otherwise):
- Nearby population within reach: {nearby_population}
- Existing competitors in this category locally: {competitor_count}
- Average local price for this category: {avg_price}
- Estimated potential customers for you (population & competition based): {estimated_customers}
- Is this market data illustrative/seeded: {is_illustrative}

KNOWN CATEGORY-LEVEL PATTERNS (general knowledge, not location-specific):
- Seasonal demand pattern: {seasonal_notes}
- Supply chain risk pattern: {supply_chain_risks}

Return ONLY valid JSON, no other text, matching exactly this shape:
{{
  "strengths": "2-3 short bullet points as plain text, separated by newlines (\\n)",
  "weaknesses": "2-3 short bullet points as plain text, separated by newlines (\\n)",
  "opportunities": "2-3 short bullet points as plain text, separated by newlines (\\n)",
  "threats": "2-3 short bullet points as plain text, separated by newlines (\\n)"
}}

Ground every point in the facts given above — do not fabricate numbers or claims
beyond what is provided. Use plain language suitable for a first-time entrepreneur.
"""


def generate_swot(
    business_category: str,
    project_cost: float,
    loan_amount: float,
    location: dict,
    market_data: dict | None = None,
    experience_level: str = "intermediate",
    competitor_mapping: dict | None = None,
    mandi_mapping: dict | None = None,
    audience_mapping: dict | None = None,
) -> dict:
    """
    location: {"village_name", "block", "district", "state"}
    market_data: {"nearby_population", "competitor_count", "avg_price", "is_illustrative"} or None

    Returns: {"strengths": str, "weaknesses": str, "opportunities": str, "threats": str}
    """
    category_notes = get_category_notes(business_category)
    market_data = market_data or {}

    if competitor_mapping is not None and competitor_mapping.get("competitor_count") is not None:
        market_data = {
            **market_data,
            "competitor_count": competitor_mapping["competitor_count"],
            "is_illustrative": False,  # this came from live OSM data, not seed data
        }

    if mandi_mapping is not None and mandi_mapping.get("avg_price") is not None:
        market_data = {
            **market_data,
            "avg_price": mandi_mapping["avg_price"],
            "is_illustrative": False,  # this came from live Agmarknet data, not seed data
        }

    style_instruction = EXPERIENCE_STYLE_GUIDANCE.get(
        experience_level, EXPERIENCE_STYLE_GUIDANCE["intermediate"]
    )

    prompt = SWOT_PROMPT.format(
        business_category=business_category,
        village_name=location.get("village_name", "Unknown"),
        block=location.get("block", "Unknown"),
        district=location.get("district", "Unknown"),
        state=location.get("state", "Unknown"),
        project_cost=project_cost,
        loan_amount=loan_amount,
        nearby_population=market_data.get("nearby_population", "Not available"),
        competitor_count=market_data.get("competitor_count", "Not available"),
        avg_price=market_data.get("avg_price", "Not available"),
        estimated_customers=market_data.get("estimated_customers", "Not available"),
        is_illustrative=market_data.get("is_illustrative", True),
        seasonal_notes=category_notes["seasonal_notes"],
        supply_chain_risks=category_notes["supply_chain_risks"],
    ) + f"\n\nSTYLE INSTRUCTION: {style_instruction}"

    response = call_gemini_with_retry(
        client.models.generate_content,
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    return json.loads(response.text)