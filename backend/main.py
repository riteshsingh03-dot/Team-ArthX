from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

from engines.eligibility.scheme_selection import select_scheme
from engines.eligibility.rules import check_eligibility
from engines.financial.loan import calculate_loan_structure
from engines.financial.repayment import generate_repayment_schedule
from engines.financial.exceptions import InvalidFinancialInput

from engines.llm.swot import generate_swot
from engines.llm.extraction import extract_user_intent
from engines.llm.explanation import generate_explanation
from engines.retrieval.search import search_scheme_documents
from engines.financial.sensitivity import compare_scenarios, run_sensitivity_analysis

from engines.journal.entries import add_journal_entry, get_entries
from engines.journal.query import answer_journal_question

from google.genai.errors import ServerError

from engines.market.mandi_price_service import get_mandi_price_mapping
from engines.market.audience_service import get_target_audience_mapping

from engines.financial.cashflow import simulate_survival

from engines.market.competitor_service import (
    refresh_competitors,
    get_stored_competitors,
    resolve_location_id,
    get_location,
    list_all_locations,
)

from engines.market.sector_ranking import rank_sectors

app = FastAPI()

# --- ENABLE CORS FOR FRONTEND CONNECTION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (e.g., your Live Server port)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SurvivalSimRequest(BaseModel):
    initial_cash: float
    base_monthly_revenue: float
    base_monthly_expenses: float
    emi: float = 0
    iterations: int = 1000
    months: int = 12

class SensitivityRequest(BaseModel):
    base_inputs: dict
    vary_field: str
    values: list[float]


class ScenarioComparisonRequest(BaseModel):
    base_inputs: dict
    scenarios: dict[str, dict]


class ChatRequest(BaseModel):
    message: str
    experience_level: str = "intermediate"
    location_id: int | None = None


class JournalEntryRequest(BaseModel):
    entry_date: str
    sales_revenue: float | None = None
    expenses: float | None = None
    units_sold: float | None = None
    notes: str | None = None


class JournalQuestionRequest(BaseModel):
    question: str


class FeasibilityRequest(BaseModel):
    state: str
    business_category: str
    margin_pct: float = 0.10
    project_cost: float | None = None
    margin_capital: float | None = None
    experience_level: str = "intermediate"
    location_id: int | None = None

class SectorScanRequest(BaseModel):
    project_cost: float
    margin_pct: float = 0.10
    location_id: int | None = None
    district: str | None = None
    village_name: str | None = None
    experience_level: str = "intermediate"
    categories: list[str] | None = None

def get_competitor_mapping(location_id: int | None, business_category: str | None) -> dict | None:
    if location_id is None or business_category is None:
        return None
    try:
        rows = get_stored_competitors(location_id, business_category)
        if not rows:
            refresh_competitors(location_id, business_category)
            rows = get_stored_competitors(location_id, business_category)
        return {
            "competitor_count": len(rows),
            "nearest": rows[:5],
        }
    except ValueError:
        return None  # bad location_id -- nothing we can do
    except RuntimeError as e:
        return {"competitor_count": None, "nearest": [], "error": "osm_temporarily_unavailable", "detail": str(e)}

def get_mandi_mapping(location_id: int | None, business_category: str | None) -> dict | None:
    return get_mandi_price_mapping(location_id, business_category)

def get_audience_mapping(location_id: int | None, fallback_district: str | None, fallback_village: str | None,
                          business_category: str | None, competitor_mapping: dict | None) -> dict | None:
    district = fallback_district or fallback_village
    if location_id is not None:
        try:
            location = get_location(location_id)
            district = location.get("district") or fallback_district
        except ValueError:
            pass  # bad location_id -- fall back to whatever the LLM extracted
    competitor_count = competitor_mapping.get("competitor_count") if competitor_mapping else None
    return get_target_audience_mapping(district, business_category, competitor_count)


@app.post("/feasibility")
def get_feasibility(req: FeasibilityRequest):
    if req.project_cost is None:
        if req.margin_capital is None:
            raise HTTPException(status_code=400, detail="Provide either project_cost or margin_capital.")
        if not (0 < req.margin_pct < 1):
            raise HTTPException(status_code=400, detail="margin_pct must be between 0 and 1 (exclusive) to derive project_cost.")
        req.project_cost = req.margin_capital / req.margin_pct

    scheme = select_scheme(project_cost=req.project_cost, state=req.state)
    if scheme is None:
        raise HTTPException(status_code=404, detail="No matching scheme found for this project cost/state.")

    user_profile = {
        "project_cost": req.project_cost,
        "state": req.state,
        "business_category": req.business_category,
    }
    eligibility = check_eligibility(user_profile, scheme["id"])

    competitor_mapping = get_competitor_mapping(req.location_id, req.business_category)

    try:
        loan = calculate_loan_structure(req.project_cost, req.margin_pct)
        schedule, installment = generate_repayment_schedule(
            principal=loan["loan_amount"],
            annual_rate_pct=float(scheme["interest_rate"]),
            tenure_months=scheme["tenure_months"],
            moratorium_months=scheme["moratorium_months"],
            frequency=scheme["repayment_frequency"],
        )
    except InvalidFinancialInput as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "scheme": {"name": scheme["name"], "interest_rate": scheme["interest_rate"], "is_illustrative": scheme.get("is_illustrative", False)},
        "eligibility": eligibility,
        "loan": loan,
        "installment": installment,
        "repayment_schedule": schedule,
        "competitor_mapping": competitor_mapping,
    }


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        extracted = extract_user_intent(req.message)
    except (json.JSONDecodeError, KeyError, IndexError):
        raise HTTPException(status_code=502, detail="Could not understand the message right now. Please try rephrasing.")
    except ServerError:
        raise HTTPException(status_code=503, detail="AI service is temporarily busy. Please try again in a moment.")

    resolved_location_id = req.location_id or resolve_location_id(
        village_name=extracted.get("village_name"),
        block=extracted.get("block"),
        district=extracted.get("district"),
    )

    # If project_cost wasn't stated but margin_capital was, derive it
    if extracted.get("project_cost") is None and extracted.get("margin_capital") is not None:
        margin_pct = 0.10  # or read from a default/config
        extracted["project_cost"] = extracted["margin_capital"] / margin_pct

    if extracted.get("project_cost") is None:
        raise HTTPException(status_code=400, detail="Could not determine project cost or available capital from your message.")

    scheme = select_scheme(project_cost=extracted["project_cost"], state=extracted.get("state"))
    if scheme is None:
        raise HTTPException(status_code=404, detail="No matching scheme found.")

    user_profile = {
        "project_cost": extracted["project_cost"],
        "state": extracted.get("state"),
        "business_category": extracted.get("business_category"),
    }

    competitor_mapping = get_competitor_mapping(resolved_location_id, extracted.get("business_category"))
    mandi_mapping = get_mandi_mapping(resolved_location_id, extracted.get("business_category"))
    audience_mapping = get_audience_mapping(
    resolved_location_id, extracted.get("district"), extracted.get("village_name"),
    extracted.get("business_category"), competitor_mapping
    )
    eligibility = check_eligibility(user_profile, scheme["id"])

    loan = calculate_loan_structure(extracted["project_cost"], extracted.get("margin_pct", 0.10))
    schedule, installment = generate_repayment_schedule(
        principal=loan["loan_amount"],
        annual_rate_pct=float(scheme["interest_rate"]),
        tenure_months=scheme["tenure_months"],
        moratorium_months=scheme["moratorium_months"],
        frequency=scheme["repayment_frequency"],
    )

    retrieved = search_scheme_documents(req.message, scheme_id=scheme["id"], top_k=3)

    explanation = generate_explanation(
        scheme, eligibility, loan, installment, retrieved,
        experience_level=req.experience_level
    )
    swot = generate_swot(
        business_category=extracted.get("business_category"),
        project_cost=extracted["project_cost"],
        loan_amount=loan["loan_amount"],
        location={
            "village_name": extracted.get("village_name"),
            "block": extracted.get("block"),
            "district": extracted.get("district"),
            "state": extracted.get("state"),
        },
        experience_level=req.experience_level,
        competitor_mapping=competitor_mapping,
        mandi_mapping=mandi_mapping,
        audience_mapping=audience_mapping,
    )

    return {
        "explanation": explanation,
        "scheme": scheme,
        "eligibility": eligibility,
        "loan": loan,
        "installment": installment,
        "retrieved_chunks": retrieved,
        "swot": swot,
        "competitor_mapping": competitor_mapping,
        "mandi_mapping": mandi_mapping,
        "audience_mapping": audience_mapping,
    }


@app.post("/scenarios/compare")
def compare_scenarios_endpoint(req: ScenarioComparisonRequest):
    return compare_scenarios(req.base_inputs, req.scenarios)


@app.post("/scenarios/sensitivity")
def sensitivity_endpoint(req: SensitivityRequest):
    return run_sensitivity_analysis(req.base_inputs, req.vary_field, req.values)


@app.post("/journal/entry")
def create_journal_entry(req: JournalEntryRequest):
    return add_journal_entry(**req.model_dump())


@app.get("/journal/entries")
def list_journal_entries(start_date: str = None, end_date: str = None):
    return get_entries(start_date, end_date)


@app.post("/journal/ask")
def ask_journal(req: JournalQuestionRequest):
    return answer_journal_question(req.question)

@app.post("/simulate/survival")
def simulate_survival_endpoint(req: SurvivalSimRequest):
    try:
        return simulate_survival(
            initial_cash=req.initial_cash,
            base_monthly_revenue=req.base_monthly_revenue,
            base_monthly_expenses=req.base_monthly_expenses,
            emi=req.emi,
            months=req.months,
            iterations=req.iterations,
        )
    except InvalidFinancialInput as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/locations")
def get_locations():
    return list_all_locations()

@app.post("/sector-scan")
def sector_scan(req: SectorScanRequest):
    try:
        return rank_sectors(
            location_id=req.location_id,
            project_cost=req.project_cost,
            margin_pct=req.margin_pct,
            district=req.district,
            village_name=req.village_name,
            categories=req.categories,
            experience_level=req.experience_level,
        )
    except InvalidFinancialInput as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ServerError:
        raise HTTPException(status_code=503, detail="AI service is temporarily busy. Please try again in a moment.")

@app.get("/health")
def health_check():
    return {"status": "ok"}